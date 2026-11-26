// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract DonationJars {
    mapping(address => uint256) public balances;
    event Donated(address indexed sender, address indexed recipient, uint256 amount);
    event Withdrawn(address indexed recipient, uint256 amount);

    function donate(address recipient) external payable {
        require(recipient != address(0), "Invalid recipient");
        require(msg.value > 0, "Empty donation");
        balances[recipient] += msg.value;
        emit Donated(msg.sender, recipient, msg.value);
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Empty jar");
        balances[msg.sender] = 0;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Withdrawal failed");
        emit Withdrawn(msg.sender, amount);
    }
}
