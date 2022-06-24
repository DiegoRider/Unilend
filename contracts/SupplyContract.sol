// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.15;

import "@openzeppelin/contracts/utils/math/Math.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
//import "@uniswapp/contracts/NonfungiblePositionManager.sol";


contract SupplyContract {
    address public immutable supplyToken;
    mapping(address => uint256) public deposits;

    constructor(address supplyToken_) {
        supplyToken = supplyToken_;
    }

    function deposit(uint256 amount) public payable {
        require(ERC20(supplyToken).transferFrom(msg.sender, address(this), amount), "transfer failed");
        deposits[msg.sender] += amount;
    }

    function doMath() public pure returns(uint256) {
        uint256 a = 12;
        uint256 b = 10;
        uint256 mx = Math.max(a, b);
        return mx;
    }
}