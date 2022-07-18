from brownie import *
from brownie import TestToken, SupplyContract, project, accounts
from web3 import EthereumTesterProvider
from pathlib import Path
import math

def main():
    # on déploie 2 tokens (pour pouvoir créer une position uniswap v3)
    token_a = TestToken.deploy({'from': accounts[0]})
    token_b = TestToken.deploy({'from': accounts[0]})

    
    # on mint les tokens sur <> addresses
    for i in range(5):
        token_a.mint(accounts[i], 10*1e18)
        token_b.mint(accounts[i], 10*1e18)

    # -------------------------------------------------------
    # on créer une pool uniswap-v3
    # -------------------------------------------------------
    #address _factory
    uniswap_core = project.load("Uniswap/v3-core@1.0.0")
    UniFactory = uniswap_core.UniswapV3Factory
    uni_factory = UniFactory.deploy({"from": accounts[0]})
    print(uni_factory)

    #address _WETH9
    weth9 = accounts[0]
    print(weth9)

    #address _tokenDescriptor_
    tokenDescriptor = accounts[0]
    print(tokenDescriptor)

    '''
    sqrtPriceX96 = sqrt(price) * 2 ** 96
    # divide both sides by 2 ** 96
    sqrtPriceX96 / (2 ** 96) = sqrt(price)
    # square both sides
    (sqrtPriceX96 / (2 ** 96)) ** 2 = price
    # expand the squared fraction
    (sqrtPriceX96 ** 2) / ((2 ** 96) ** 2)  = price
    # multiply the exponents in the denominator to get the final expression
    sqrtRatioX96 ** 2 / 2 ** 192 = price
    '''

    # params 
    fee_list = [500, 3000, 10000]
    
    # vars
    price = 1.2654
    fee = fee_list[1]

    # fonctions
    def sqrtRatioX96_ofPrice(price):
        return math.sqrt(price) * 2 ** 96
    x96_price = sqrtRatioX96_ofPrice(price)

    # NonFungiblePositionManager
    nfPosManager = project.load("Uniswap/v3-periphery@1.0.0").NonfungiblePositionManager
    myPosManager = nfPosManager.deploy(uni_factory, weth9, tokenDescriptor, {"from": accounts[0]})
    print(myPosManager)

    # initialize pool
    myPosManager.createAndInitializePoolIfNecessary(token_a, token_b, fee, x96_price, {"from": accounts[0]})

