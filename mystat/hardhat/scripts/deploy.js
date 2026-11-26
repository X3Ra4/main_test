const { ethers } = require("hardhat");

async function main() {
  const [seller] = await ethers.getSigners();
  const auction = await ethers.deployContract("DutchAuction", [seller.address, 1000, 2, 100, 800]);
  const voting = await ethers.deployContract("Voting", [3600]);
  await Promise.all([auction.waitForDeployment(), voting.waitForDeployment()]);
  console.log("DutchAuction:", await auction.getAddress());
  console.log("Voting:", await voting.getAddress());
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
