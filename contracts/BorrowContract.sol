// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.7.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@linkedlist/contracts/StructuredLinkedList.sol";

contract BorrowContract is ERC721, Ownable {

    mapping(uint256 => Loan) private _loans; // all deposits
    uint256 private _nextDepositId = 1;
    address borrowContract;

    using StructuredLinkedList for StructuredLinkedList.List;
    StructuredLinkedList.List private _loanList; // active loans sorted by expiration

    struct Loan {
        uint256 collateralId;
        uint256 amount;
        uint256 expiration;
        uint256 interestRateBPS;
    }

    mapping(address => uint256) public borrowLimit; // whitelist + limit

    constructor(address borrowContract_) ERC721("UnilendLoanNFT", "ULL") {
        borrowContract = borrowContract_;
    }


    function openLoan(uint256 positionId, uint256 expiration, uint256 amount) public {
        
        // verify value of position > amount * collateral ratio
        // verify amount is available in borrow contract
        // transfer ownership of positionId to BorrowContract
        // transfer loan to sender
        // mint loan NFT

    }

    function closeLoan(uint256 positionId) public {

        // compute debt
        // repay loan
        // transfer position NFT back
        // burn loan NFT

    }

    function repayLoan(uint256 amount) public {

        // transfer tokens
        // adjust state

    }

    function borrowMore(uint256 amount) public {

        // verify enough collateral
        // transfer tokens
        // adjust state

    }

    function liquidate(uint256 positionId) public {

        // verify liquidation conditions are valid
        // reimburse debt 
        // transfer position to liquidator

    }

    function positionValue(uint256 positionId) private returns(uint256) {
        return 0;
    }

    function isLiquidityAvailable(uint256 expiration) private returns(uint256) {
        return 0;
    }

}