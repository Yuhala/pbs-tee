// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";

import "../src/HelloWorld.sol";

contract DeployHelloWorld is Script {
    function run() external {
        // Start broadcasting transactions
        vm.startBroadcast();

        // Deploy contract with constructor argument
        HelloWorld hello = new HelloWorld("Hello from Foundry!");

        // Stop broadcasting
        vm.stopBroadcast();

        // Print the deployed contract address
        console.log("Deployed HelloWorld at:", address(hello));
    }
}