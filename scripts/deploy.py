from brownie import *
from brownie import TestToken, SupplyContract

def main():

    token = accounts[0].deploy(TestToken)
    for i in range(5):
        token.mint(accounts[i], 1000)

    supply_contract = accounts[0].deploy(SupplyContract, token)

    token.approve(supply_contract, 2**256 - 1, {'from':accounts[1]})
    supply_contract.depositAndLock(100, 20, 0, {'from': accounts[1]})