from logging import exception
from brownie import *
from brownie import TestToken, SupplyContract, project, accounts, UniUtils
from eth_typing import BlockNumber
#from web3 import *
#import web3.eth as wweb3
from pathlib import Path
import math

FEE_LIST = [500, 3000, 10000]
TICK_SPACING_LIST = [10, 60, 200]

def print_events(tx):
    for key in tx.events.keys():
        print(key)
        for item in tx.events[key]:
            print(item)

def getTick(uni_utils, price, spacing, floor=True): 
    tick = uni_utils.ratioToTick(sqrtRatioX96_ofPrice(price))
    if floor == True:
        tick = tick - tick % spacing
    else:
        tick = tick + (-tick) % spacing
    return tick

def sqrtRatioX96_ofPrice(price):
    return math.sqrt(price) * 2 ** 96

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



def main():
    print("deploying erc20 tokens")
    token_a = TestToken.deploy({'from': accounts[0]})
    token_b = TestToken.deploy({'from': accounts[0]})

    print("minting erc20 tokens")
    for i in range(3):
        token_a.mint(accounts[i], 10*1e18)
        token_b.mint(accounts[i], 10*1e18)

    print("deploying uniswap utility contract")
    uni_utils = UniUtils.deploy({"from": accounts[0]})

    print("deploying uniswap factory")
    uniswap_core = project.load("Uniswap/v3-core@1.0.0")
    uni_factory = uniswap_core.UniswapV3Factory.deploy({"from": accounts[0]})
    weth9 = accounts[0]
    tokenDescriptor = accounts[0]
    
    print("depoying NonfungiblePositionManager")
    nft_pos_manager = project.load("Uniswap/v3-periphery@1.0.0").NonfungiblePositionManager
    pos_manager = nft_pos_manager.deploy(uni_factory, weth9, tokenDescriptor, {"from": accounts[0]})

    # pool parameters
    price = 1.2654
    fee = FEE_LIST[1]
    tick_spacing = TICK_SPACING_LIST[1]

    print("initializing pool")
    my_pool_add = pos_manager.createAndInitializePoolIfNecessary(
        token_a, 
        token_b, 
        fee, 
        sqrtRatioX96_ofPrice(price), 
        {"from": accounts[0]}
    )
    print("pool created events: ")
    print_events(my_pool_add)

    print("adding liquidity")
    # # params
    min_price = 1
    max_price = 2
    
    # #block_number = web3.eth.block_number
    # #block_timestamp = web3.eth.get_block(block_number).timestamp
    
    token_a.approve(pos_manager, 2**256 - 1, {'from':accounts[1]})
    token_b.approve(pos_manager, 2**256 - 1, {'from':accounts[1]})

    # for mint to work, you may have to edit v3-periphery/contracts/libraries/PoolAddress.sol:
    # bytes32 internal constant POOL_INIT_CODE_HASH = 0x67ab6764c0956bbe32399c32e0100e6e9a162929035bcf8cd5bbed5debfff967;
    # POOL_INIT_CODE_HASH = keccak256(abi.encodePacked(type(UniswapV3Pool).creationCode)); in v3-core/contracts/UniswapV3PoolDeployer.sol
    my_pos = pos_manager.mint(
        (
            token_a, # token0
            token_b, # token1
            fee, # fee
            getTick(uni_utils, min_price, tick_spacing, floor=True), # tickLower
            getTick(uni_utils, max_price, tick_spacing, floor=False), # tickLower
            1*1e18, # amount0Desired
            1*1e18, # amount1Desired
            0, # amount0Min
            0, # amount1Min
            accounts[1].address, # recipient
            10000000000000 # deadline
        ),
        {
            "from": accounts[1]
        }
    )
    print_events(my_pos)

    # swap(s)
    raise Exception