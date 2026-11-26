import hashlib
import json
import time
from dataclasses import asdict, dataclass, replace


@dataclass(frozen=True)
class Block:
    index: int
    timestamp: int
    data: tuple
    prev_hash: str
    nonce: int = 0
    hash: str = ""

    def compute_hash(self):
        fields = asdict(self)
        del fields["hash"]
        return hashlib.sha256(json.dumps(fields, ensure_ascii=False, sort_keys=True,
                                         separators=(",", ":")).encode()).hexdigest()

    @classmethod
    def from_dict(cls, payload):
        return cls(**{**payload, "data": tuple(payload["data"])})


class Blockchain:
    def __init__(self, difficulty=3):
        if not 1 <= difficulty <= 6:
            raise ValueError("Difficulty must be in 1..6")
        self.difficulty = difficulty
        genesis = Block(0, 0, ("Genesis",), "0" * 64)
        self.chain = [replace(genesis, hash=genesis.compute_hash())]
        self.genesis = self.chain[0]

    @property
    def last_block(self):
        return self.chain[-1]

    def follows(self, block, previous):
        return (block.index == previous.index + 1 and block.prev_hash == previous.hash
                and block.timestamp >= previous.timestamp and block.nonce >= 0
                and block.hash == block.compute_hash() and block.hash.startswith("0" * self.difficulty))

    def add_block(self, block):
        if not self.follows(block, self.last_block):
            return False
        self.chain.append(block)
        return True

    def is_chain_valid(self, blocks=None):
        blocks = self.chain if blocks is None else blocks
        return bool(blocks and blocks[0] == self.genesis and
                    all(self.follows(current, previous) for previous, current in zip(blocks, blocks[1:])))

    def replace_chain(self, candidate):
        if len(candidate) <= len(self.chain) or not self.is_chain_valid(candidate):
            return False
        self.chain = list(candidate)
        return True


class Miner:
    def __init__(self, name):
        self.name = name

    def mine_block(self, data, blockchain):
        return self.mine_candidate(tuple(data), blockchain.last_block, blockchain.difficulty)

    def mine_candidate(self, items, previous, difficulty):
        candidate = Block(previous.index + 1, max(time.time_ns(), previous.timestamp), items, previous.hash)
        prefix = "0" * difficulty
        nonce = 0
        while True:
            current = replace(candidate, nonce=nonce)
            digest = current.compute_hash()
            if digest.startswith(prefix):
                return replace(current, hash=digest)
            nonce += 1
