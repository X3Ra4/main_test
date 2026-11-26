// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract BoardVoting {
    struct Proposal {
        string description;
        uint256 yesVotes;
        uint256 noVotes;
    }

    address public immutable chair;
    mapping(address => bool) public isDirector;
    address[] private directors;
    Proposal[] private proposals;
    mapping(uint256 => mapping(address => bool)) public voted;
    event VoteCast(uint256 indexed proposalId, address indexed director, bool support);

    constructor(address[] memory members) {
        require(members.length != 0, "Empty board");
        chair = msg.sender;
        for (uint256 i; i < members.length; ++i) {
            address member = members[i];
            require(member != address(0) && !isDirector[member], "Invalid director");
            isDirector[member] = true;
            directors.push(member);
        }
    }

    function listDirectors() external view returns (address[] memory) {
        return directors;
    }

    function propose(string calldata description) external returns (uint256) {
        require(msg.sender == chair, "Only chair");
        require(bytes(description).length != 0, "Empty proposal");
        proposals.push(Proposal(description, 0, 0));
        return proposals.length - 1;
    }

    function vote(uint256 id, bool support) external {
        require(isDirector[msg.sender], "Only directors");
        require(id < proposals.length, "Unknown proposal");
        require(!voted[id][msg.sender], "Already voted");
        voted[id][msg.sender] = true;
        if (support) ++proposals[id].yesVotes;
        else ++proposals[id].noVotes;
        emit VoteCast(id, msg.sender, support);
    }

    function results(uint256 id) external view returns (Proposal memory) {
        require(id < proposals.length, "Unknown proposal");
        return proposals[id];
    }
}
