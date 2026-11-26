// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Voting {
    struct Candidate { string name; uint256 votes; }

    address public immutable owner = msg.sender;
    uint256 public immutable deadline;
    Candidate[] public candidates;
    mapping(address => bool) public hasVoted;
    mapping(bytes32 => bool) private registered;

    event CandidateAdded(uint256 indexed candidateId, string name);
    event Voted(address indexed voter, uint256 indexed candidateId);

    constructor(uint256 duration) {
        require(duration > 0, "Invalid duration");
        deadline = block.timestamp + duration;
    }

    function addCandidate(string calldata name) external {
        require(msg.sender == owner, "Only owner");
        require(block.timestamp < deadline, "Voting closed");
        require(bytes(name).length > 0 && bytes(name).length <= 64, "Invalid name");
        bytes32 nameHash = keccak256(bytes(name));
        require(!registered[nameHash], "Candidate exists");
        registered[nameHash] = true;
        candidates.push(Candidate(name, 0));
        emit CandidateAdded(candidates.length - 1, name);
    }

    function vote(uint256 candidateId) external {
        require(block.timestamp < deadline, "Voting closed");
        require(candidateId < candidates.length, "Unknown candidate");
        require(!hasVoted[msg.sender], "Already voted");
        hasVoted[msg.sender] = true;
        candidates[candidateId].votes += 1;
        emit Voted(msg.sender, candidateId);
    }

    function winner() external view returns (uint256 id, string memory name, uint256 votes) {
        require(block.timestamp >= deadline, "Voting still open");
        uint256 count = candidates.length;
        bool tied;
        for (uint256 index = 0; index < count; index++) {
            uint256 received = candidates[index].votes;
            if (received > votes) {
                id = index;
                votes = received;
                tied = false;
            } else if (received == votes) {
                tied = true;
            }
        }
        require(votes > 0, "No votes");
        require(!tied, "Tie");
        return (id, candidates[id].name, votes);
    }
}
