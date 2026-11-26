const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture, time } = require("@nomicfoundation/hardhat-network-helpers");

describe("DutchAuction", function () {
  async function deploy() {
    const [seller, buyer, other] = await ethers.getSigners();
    const auction = await ethers.deployContract("DutchAuction", [seller.address, 1000, 2, 100, 800]);
    await auction.waitForDeployment();
    return { auction, seller, buyer, other };
  }

  it("starts at the maximum and decreases at the chosen rate", async function () {
    const { auction } = await loadFixture(deploy);
    expect(await auction.getPrice()).to.equal(1000n);
    await time.increase(25);
    expect(await auction.getPrice()).to.equal(950n);
  });

  it("pays the seller, refunds the excess and records the first buyer", async function () {
    const { auction, seller, buyer, other } = await loadFixture(deploy);
    await time.setNextBlockTimestamp(Number(await auction.startTime()) + 10);
    await expect(auction.connect(buyer).buy({ value: 1100 }))
      .to.changeEtherBalances([seller, buyer, auction], [980n, -980n, 0n]);
    expect(await auction.buyer()).to.equal(buyer.address);
    expect(await auction.ended()).to.equal(true);
    await expect(auction.connect(other).buy({ value: 1100 })).to.be.revertedWith("Auction ended");
  });

  it("rejects underpayment and lets only the seller close an expired auction", async function () {
    const { auction, buyer } = await loadFixture(deploy);
    await expect(auction.connect(buyer).buy({ value: 1 })).to.be.revertedWith("Insufficient payment");
    await expect(auction.claimRefund()).to.be.revertedWith("Auction still running");
    await time.increaseTo(Number(await auction.endTime()));
    expect(await auction.getPrice()).to.equal(800n);
    await expect(auction.connect(buyer).buy({ value: 1100 })).to.be.revertedWith("Auction expired");
    await expect(auction.connect(buyer).claimRefund()).to.be.revertedWith("Only seller");
    await auction.claimRefund();
    expect(await auction.ended()).to.equal(true);
  });

  it("rejects a discount that would cross the reserve price", async function () {
    const [seller] = await ethers.getSigners();
    const Auction = await ethers.getContractFactory("DutchAuction");
    await expect(Auction.deploy(seller.address, 1000, 3, 100, 800))
      .to.be.revertedWith("Discount below reserve");
  });
});
