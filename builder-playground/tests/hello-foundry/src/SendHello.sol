// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract SendHello {
    string public message;

    constructor() {
        message = "Hello World";
    }

    function setMessage(string memory newMessage) public {
        message = newMessage;
    }
}

//Deployer: 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720
//Deployed to: 0xA7e3FFB41Db860Fd0D97186e0c3De1E424c96C9f
//Transaction hash: 0x4a042c06d1f1f9b05af086901eadaa6783c384aadb3d5cec41b449367313ca66
