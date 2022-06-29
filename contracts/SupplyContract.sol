// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.7.6;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@uniswap/periphery/contracts/NonfungiblePositionManager.sol";
// import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";


contract SupplyContract is ERC721, Ownable {
    address public immutable supplyToken;
    mapping(uint256 => LockedDeposit) private _deposits;
    uint256 private _nextId = 1;

    // using EnumerableSet for EnumerableSet.UintSet;
    // EnumerableSet.UintSet private _liveDepositIds;

    struct LockedDeposit {
        uint256 amount;
        uint256 releaseTime;
    }

    constructor(address supplyToken_) ERC721("UnilendDepositNFT", "ULD") {
        supplyToken = supplyToken_;
    }

    function depositAndLock(uint256 amount, uint256 releaseTime) public {
        require(ERC20(supplyToken).transferFrom(msg.sender, address(this), amount), "transfer failed");
        
        uint256 tokenId = _nextId++;

        _safeMint(msg.sender, tokenId);
        // _liveDepositIds.add(tokenId);
        _deposits[tokenId] = LockedDeposit({
            amount:amount,
            releaseTime:releaseTime
        });
    }

    function withdraw(uint256 tokenId) public {
        
        LockedDeposit memory deposit = _deposits[tokenId];
        require(ownerOf(tokenId) == msg.sender);
        require(deposit.releaseTime <= block.timestamp);
        require(ERC20(supplyToken).transferFrom( address(this), msg.sender, deposit.amount), "transfer failed");
        _burn(tokenId);
        // _liveDepositIds.remove(tokenId);
        
    }

    function getLiquidity(uint256 timestamp) public view returns(uint256) {
        uint256 totalLiquidity = 0;
        // for(uint i=0; i<_liveDepositIds.length(); i++){
        //     if( _deposits[_liveDepositIds.at(i)].releaseTime > timestamp) {
        //         totalLiquidity += _deposits[i].amount;
        //     }
        // }
        return totalLiquidity;
    }

}