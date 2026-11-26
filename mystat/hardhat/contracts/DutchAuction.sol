// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract DutchAuction {
    address payable public immutable seller;
    uint256 public immutable startPrice;
    uint256 public immutable discountRate;
    uint256 public immutable reservePrice;
    uint256 public immutable startTime;
    uint256 public immutable endTime;
    bool public ended;
    address public buyer;

    event Purchased(address indexed buyer, uint256 price);
    event Closed();

    constructor(address payable seller_, uint256 startPrice_, uint256 discountRate_,
                uint256 duration, uint256 reservePrice_) {
        require(seller_ != address(0), "Invalid seller");
        require(duration > 0, "Invalid duration");
        require(startPrice_ >= reservePrice_, "Start below reserve");
        require(discountRate_ <= (startPrice_ - reservePrice_) / duration, "Discount below reserve");
        seller = seller_;
        startPrice = startPrice_;
        discountRate = discountRate_;
        reservePrice = reservePrice_;
        startTime = block.timestamp;
        endTime = block.timestamp + duration;
    }

    function getPrice() public view returns (uint256) {
        if (block.timestamp >= endTime) return reservePrice;
        return startPrice - discountRate * (block.timestamp - startTime);
    }

    function buy() external payable {
        require(!ended, "Auction ended");
        require(block.timestamp < endTime, "Auction expired");
        uint256 price = getPrice();
        require(msg.value >= price, "Insufficient payment");
        ended = true;
        buyer = msg.sender;
        uint256 refund = msg.value - price;
        (bool paid, ) = seller.call{value: price}("");
        require(paid, "Payment failed");
        if (refund > 0) {
            (bool refunded, ) = payable(msg.sender).call{value: refund}("");
            require(refunded, "Refund failed");
        }
        emit Purchased(msg.sender, price);
    }

    function claimRefund() external {
        require(msg.sender == seller, "Only seller");
        require(!ended, "Auction ended");
        require(block.timestamp >= endTime, "Auction still running");
        ended = true;
        emit Closed();
    }
}
