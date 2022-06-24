from brownie import *
from brownie import TestToken, SupplyContract

def main():
    deployed_token = TestToken.deploy({'from': accounts[0]})

    for i in range(5):
        deployed_token.mint(accounts[0], 10*1e18)

    deployed_supply = SupplyContract.deploy(deployed_token, {'from': accounts[0]})
    deployed_supply.deposit(1e18, {'from': accounts[1]})