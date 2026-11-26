import argparse
import json
import queue
import threading
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from chain import Block, Blockchain, Miner


class Mempool:
    def __init__(self):
        self.messages = queue.Queue()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        entries = {}
        while True:
            action, payload, reply = self.messages.get()
            if action == "add":
                result = payload not in entries
                if result:
                    entries[payload] = None
            elif action == "take":
                result = tuple(list(entries)[:payload])
            elif action == "drop":
                for item in payload:
                    entries.pop(item, None)
                result = None
            else:
                return
            reply.put(result)

    def call(self, action, payload):
        reply = queue.Queue(1)
        self.messages.put((action, payload, reply))
        return reply.get()


def request(peer, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    with urlopen(Request(peer + path, data, {"Content-Type": "application/json"}), timeout=2) as response:
        return json.load(response)


class Node:
    def __init__(self, peers, name):
        self.chain = Blockchain()
        self.pool = Mempool()
        self.miner = Miner(name)
        self.peers = peers
        self.lock = threading.RLock()
        self.mine_requests = queue.Queue()

    def confirmed(self):
        return {item for block in self.chain.chain[1:] for item in block.data}

    def add_transaction(self, text, relay):
        with self.lock:
            added = text not in self.confirmed() and self.pool.call("add", text)
        if added and relay:
            self.broadcast("/transaction", {"text": text, "relay": False})
        return added

    def accept_block(self, block):
        with self.lock:
            if not self.chain.add_block(block):
                return False
            self.pool.call("drop", block.data)
            return True

    def sync(self):
        updated = False
        for peer in self.peers:
            try:
                candidate = [Block.from_dict(item) for item in request(peer, "/chain")]
                with self.lock:
                    before = self.confirmed()
                    if self.chain.replace_chain(candidate):
                        after = self.confirmed()
                        self.pool.call("drop", after)
                        for item in sorted(before - after):
                            self.pool.call("add", item)
                        updated = True
            except (OSError, URLError, ValueError, TypeError, KeyError):
                continue
        return updated

    def broadcast(self, path, data):
        for peer in self.peers:
            try:
                request(peer, path, data)
            except (URLError, OSError):
                continue

    def mining_worker(self):
        while True:
            reply = self.mine_requests.get()
            with self.lock:
                items = self.pool.call("take", 10)
                previous = self.chain.last_block
            if not items:
                reply.put(None)
                continue
            block = self.miner.mine_candidate(items, previous, self.chain.difficulty)
            if self.accept_block(block):
                payload = asdict(block)
                reply.put(payload)
                self.broadcast("/block", payload)
            else:
                reply.put(None)


def handler_for(node):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, value):
            data = json.dumps(value, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/chain":
                with node.lock:
                    chain = [asdict(block) for block in node.chain.chain]
                return self.reply(200, chain)
            return self.reply(404, {"error": "Unknown route"})

        def do_POST(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 <= length <= 65536:
                    return self.reply(413, {"error": "Invalid body size"})
                payload = json.loads(self.rfile.read(length)) if length else {}
                if self.path == "/transaction":
                    text = payload["text"]
                    if not isinstance(text, str) or not 0 < len(text.strip()) <= 200:
                        return self.reply(400, {"error": "Invalid transaction"})
                    return self.reply(200, {"added": node.add_transaction(text.strip(), payload.get("relay", True))})
                if self.path == "/block":
                    return self.reply(200, {"accepted": node.accept_block(Block.from_dict(payload)) or node.sync()})
                if self.path == "/mine":
                    reply = queue.Queue(1)
                    node.mine_requests.put(reply)
                    return self.reply(200, {"block": reply.get(timeout=20)})
                if self.path == "/sync":
                    return self.reply(200, {"updated": node.sync()})
                return self.reply(404, {"error": "Unknown route"})
            except (ValueError, TypeError, KeyError, AttributeError):
                return self.reply(400, {"error": "Invalid payload"})
            except queue.Empty:
                return self.reply(503, {"error": "Mining timeout"})

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peer", action="append", default=[])
    args = parser.parse_args()
    for peer in args.peer:
        url = urlsplit(peer)
        if url.scheme != "http" or url.hostname != "127.0.0.1" or not url.port or url.path or url.query or url.fragment:
            parser.error("Peer must be http://127.0.0.1:PORT")
    node = Node(args.peer, f"miner-{args.port}")
    threading.Thread(target=node.mining_worker, daemon=True).start()
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(node)) as server:
        print(f"Node listening on 127.0.0.1:{args.port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
