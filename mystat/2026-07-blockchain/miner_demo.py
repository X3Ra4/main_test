from dataclasses import replace

from chain import Blockchain, Miner


def main():
    chain = Blockchain(difficulty=3)
    miner = Miner("Dnipro Demo")
    for batch in (["Олена -> Петро: 12"], ["Петро -> Марія: 4", "Марія -> Олена: 1"]):
        block = miner.mine_block(batch, chain)
        assert chain.add_block(block)
        print(f"{miner.name}: block #{block.index}, nonce={block.nonce}, hash={block.hash}")
        print("Транзакції:", *batch, sep="\n")
    assert chain.is_chain_valid()
    assert not chain.is_chain_valid([*chain.chain[:-1], replace(chain.last_block, data=("changed",))])
    print("Ланцюг валідний, підміну даних відхилено.")


if __name__ == "__main__":
    main()
