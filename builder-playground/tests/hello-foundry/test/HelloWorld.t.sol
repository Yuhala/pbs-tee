// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import "forge-std/Test.sol";
import "../src/HelloWorld.sol";

contract HelloWorldTest is Test {
    HelloWorld hello;

    function setUp() public {
        hello = new HelloWorld("Initial message");
    }

    function testMessage() public {
        assertEq(hello.message(), "Initial message");
    }

    function testSetMessage() public {
        hello.setMessage("New message");
        assertEq(hello.message(), "New message");
    }
}
