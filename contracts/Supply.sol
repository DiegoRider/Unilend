// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.15;

import "@openzeppelin/contracts/utils/math/Math.sol";


contract SupplyContract {
    string value;

    constructor() {
        value = "blabli";
    }

    function getValue() public view returns(string memory) {
        return value;
    }

    function setValue(string memory newValue) public {
        value = newValue;
    }

    function doMath() public pure returns(uint256) {
        uint256 a = 12;
        uint256 b = 10;
        uint256 mx = Math.max(a, b);
        return mx;
    }
}