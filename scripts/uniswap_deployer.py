from logging import exception
from brownie import *
from brownie import TestToken, SupplyContract, project, accounts, UniUtils
from eth_typing import BlockNumber
#from web3 import *
#import web3.eth as wweb3
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
    uni_factory = uniswap_core.UniswapV3Factory.deploy({"from": accounts[0]})
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
    nft_pos_manager = project.load("Uniswap/v3-periphery@1.0.0").NonfungiblePositionManager
    pos_manager = nft_pos_manager.deploy(uni_factory, weth9, tokenDescriptor, {"from": accounts[0]})
    print(pos_manager)

    # initialize pool
    my_pool_add = pos_manager.createAndInitializePoolIfNecessary(token_a, token_b, fee, x96_price, {"from": accounts[0]})

    # mon petit contrat d'utilitaires uniswap
    uni_utils = UniUtils.deploy({"from": accounts[0]})
    
    # add liq

    # params
    min_price = 1
    max_price = 2

    #block_number = web3.eth.block_number
    #block_timestamp = web3.eth.get_block(block_number).timestamp


    '''
    struct MintParams {
        address token0;
        address token1;
        uint24 fee;
        int24 tickLower;
        int24 tickUpper;
        uint256 amount0Desired;
        uint256 amount1Desired;
        uint256 amount0Min;
        uint256 amount1Min;
        address recipient;
        uint256 deadline;
    }
    '''
    
    token_a.approve(pos_manager, 2**256 - 1, {'from':accounts[1]})
    token_b.approve(pos_manager, 2**256 - 1, {'from':accounts[1]})

    my_pos = pos_manager.mint((token_b, 
    token_a, 
    fee,
    -60, # uni_utils.ratioToTick(sqrtRatioX96_ofPrice(min_price)),
    60, # uni_utils.ratioToTick(sqrtRatioX96_ofPrice(max_price)),
    1*1e18,
    1*1e18,
    0,
    0,
    accounts[1],
    10000000000000), {"from": accounts[1]})


    # swap(s)
    raise exception