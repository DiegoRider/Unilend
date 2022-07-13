// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.7.6;
pragma abicoder v2;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/math/Math.sol";
import "@uniswap/periphery/contracts/NonfungiblePositionManager.sol";
import "@linkedlist/contracts/StructuredLinkedList.sol";
import "@openzeppelin/contracts/utils/Strings.sol";


contract SupplyContract is ERC721, Ownable {
    address public immutable supplyToken;
    mapping(uint256 => Deposit) private _deposits; // all deposits
    uint256 private _nextDepositId = 1;

    using StructuredLinkedList for StructuredLinkedList.List;
    StructuredLinkedList.List private _depositList; // active deposits sorted by expiration

    struct Deposit {
        uint256 amount;
        uint256 expiration;
    }

    constructor(address supplyToken_) ERC721("UnilendDepositNFT", "ULD") {
        supplyToken = supplyToken_;
        ERC20(supplyToken_).approve(address(this), 2**256 - 1);
    }

    function depositAndLock(uint256 amount, uint256 expiration, uint256 insertAfter) public returns(uint256) {
        require(ERC20(supplyToken).transferFrom(msg.sender, address(this), amount), "transfer failed");
        
        uint256 depositId = _nextDepositId++;

        _safeMint(msg.sender, depositId);

        if(depositId > 1) {
            require(_deposits[insertAfter].expiration < expiration);
            (bool exists, uint256 next) = _depositList.getNextNode(insertAfter);
            require(exists);
            if(next > 0) {
                // console.log("my variable", next);
                require(expiration < _deposits[next].expiration, Strings.toString(next));
            }
        } else {
            require(insertAfter == 0);
        }
              
        _depositList.insertAfter(insertAfter, depositId);

        _deposits[depositId] = Deposit({
            amount:amount,
            expiration:expiration
        });

        return(depositId);
    }

    function withdraw(uint256 depositId) public {
        
        Deposit memory deposit = _deposits[depositId];
        require(ownerOf(depositId) == msg.sender);
        require(deposit.expiration <= block.timestamp);
        ERC20 token = ERC20(supplyToken);
        require(token.transferFrom( address(this), msg.sender, deposit.amount), "transfer failed");
        _burn(depositId);
        _depositList.remove(depositId);
        
    }

    event mylog(uint256 depositId, Deposit value);

    function getDeposits() public returns(Deposit[] memory){ 
        Deposit[] memory deposits = new Deposit[](_depositList.sizeOf());
        (,, uint256 next) = _depositList.getNode(0);
        uint i = 0;

        while(next > 0) {
            emit mylog(next, _deposits[next]);
            deposits[i++] = _deposits[next];
            (,, next) = _depositList.getNode(next);
        }
        return(deposits);
    }

}