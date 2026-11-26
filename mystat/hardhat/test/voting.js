const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture, time } = require("@nomicfoundation/hardhat-network-helpers");

describe("Voting", function () {
  async function deploy() {
    const [, voterA, voterB, voterC] = await ethers.getSigners();
    const voting = await ethers.deployContract("Voting", [100]);
    await voting.addCandidate("Олена");
    await voting.addCandidate("Андрій");
    return { voting, voterA, voterB, voterC };
  }

  it("counts votes and announces the winner at the deadline", async function () {
    const { voting, voterA, voterB, voterC } = await loadFixture(deploy);
    await voting.connect(voterA).vote(0);
    await voting.connect(voterB).vote(1);
    await voting.connect(voterC).vote(0);
    await expect(voting.winner()).to.be.revertedWith("Voting still open");
    await time.increaseTo(Number(await voting.deadline()));
    expect(await voting.winner()).to.deep.equal([0n, "Олена", 2n]);
    await expect(voting.connect(voterA).vote(1)).to.be.revertedWith("Voting closed");
  });

  it("rejects invalid input and unauthorized candidate registration", async function () {
    const { voting, voterA } = await loadFixture(deploy);
    await expect(voting.connect(voterA).addCandidate("Іван")).to.be.revertedWith("Only owner");
    await expect(voting.addCandidate("")).to.be.revertedWith("Invalid name");
    await expect(voting.addCandidate("Олена")).to.be.revertedWith("Candidate exists");
    await expect(voting.vote(2)).to.be.revertedWith("Unknown candidate");
  });

  it("preserves one vote per address even across different candidates", async function () {
    const { voting, voterA } = await loadFixture(deploy);
    await voting.connect(voterA).vote(0);
    await expect(voting.connect(voterA).vote(1)).to.be.revertedWith("Already voted");
    expect((await voting.candidates(0)).votes).to.equal(1n);
    expect((await voting.candidates(1)).votes).to.equal(0n);
  });

  it("reports no winner for an empty poll or a tie", async function () {
    const { voting, voterA, voterB } = await loadFixture(deploy);
    const empty = await ethers.deployContract("Voting", [100]);
    await voting.connect(voterA).vote(0);
    await voting.connect(voterB).vote(1);
    await time.increaseTo(Number(await empty.deadline()));
    await expect(voting.winner()).to.be.revertedWith("Tie");
    await expect(empty.winner()).to.be.revertedWith("No votes");
  });
});
