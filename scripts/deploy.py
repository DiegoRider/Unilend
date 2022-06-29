from brownie import *
from brownie import TestToken, SupplyContract

def main():
    deployed_token = TestToken.deploy({'from': accounts[0]})

    for i in range(2):
        deployed_token.mint(accounts[i], 10*1e18)

    deployed_supply = SupplyContract.deploy(deployed_token, {'from': accounts[0]})

    deployed_token.approve(deployed_supply, 2**256 - 1, {'from':accounts[1]})
    # uint256 MAX_INT = 2**256 - 1;
    # ERC20(supplyToken).approve(address(this), MAX_INT);

    deployed_supply.depositAndLock(1e18, 10, {'from': accounts[1]})