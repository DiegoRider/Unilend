from brownie import accounts, SupplyContract, TestToken
import pytest


def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

@pytest.fixture
def supply_contract():
    deployed_token = accounts[0].deploy(TestToken)
    return accounts[0].deploy(SupplyContract, deployed_token)

def test_supply(supply_contract):
    print(supply_contract)
    output = supply_contract.getLiquidity(10)
    print(output)
    assert output == 0

    



