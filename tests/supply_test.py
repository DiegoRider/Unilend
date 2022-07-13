from brownie import accounts, SupplyContract, TestToken
import pytest

INIT_BALANCE = 1000

def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

@pytest.fixture
def token():
    return accounts[0].deploy(TestToken)

@pytest.fixture
def distribute_tokens(token):
    for i in range(5):
        token.mint(accounts[i], INIT_BALANCE)

@pytest.fixture
def supply_contract(token):
    return accounts[0].deploy(SupplyContract, token)

def test_deposit_withdraw(supply_contract, token, distribute_tokens):
    amount_1 = 50
    amount_2 = 200
    amount_3 = 10
    expiration_1 = 20
    expiration_2 = 100
    expiration_3 = 50
    
    token.approve(supply_contract, 2**256 - 1, {'from':accounts[1]})
    deposit1 = supply_contract.depositAndLock(amount_1, expiration_1, 0, {'from': accounts[1]}).return_value
    assert token.balanceOf(accounts[1]) == INIT_BALANCE - amount_1

    deposit2 = supply_contract.depositAndLock(amount_2, expiration_2, deposit1, {'from': accounts[1]}).return_value
    assert token.balanceOf(accounts[1]) == INIT_BALANCE - amount_1 - amount_2

    token.approve(supply_contract, 2**256 - 1, {'from':accounts[2]})
    deposit3 = supply_contract.depositAndLock(amount_3, expiration_3, deposit1, {'from': accounts[2]}).return_value
    assert token.balanceOf(accounts[2]) == INIT_BALANCE - amount_3

    supply_contract.withdraw(deposit2, {'from': accounts[1]})
    assert token.balanceOf(accounts[1]) == INIT_BALANCE - amount_1

    deposits = supply_contract.getDeposits({'from': accounts[1]}).return_value
    assert deposits == ((amount_1, expiration_1), (amount_3, expiration_3))







    



