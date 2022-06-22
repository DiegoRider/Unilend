from brownie import accounts, SupplyContract
import pytest


def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

@pytest.fixture
def supply_contract():
    return accounts[0].deploy(SupplyContract)

def test_supply(supply_contract):
    output = supply_contract.doMath()
    assert output == 12

    



