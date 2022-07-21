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

def get_tick(uni_utils, price, spacing, floor=True): 
    tick = uni_utils.ratioToTick(sqrt_ratio_x96(price))
    if floor == True:
        tick = tick - tick % spacing
    else:
        tick = tick + (-tick) % spacing
    return tick

def sqrt_ratio_x96(price):
    return math.sqrt(price) * 2 ** 96


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
    
    
    print("depoying NonfungiblePositionManager")
    uniswap_periphery = project.load("Uniswap/v3-periphery@1.0.0")
    uniswap_periphery.NFTDescriptor.deploy({"from": accounts[0]})
    tokenDescriptor = uniswap_periphery.NonfungibleTokenPositionDescriptor.deploy(weth9, {"from": accounts[0]})
    pos_manager = uniswap_periphery.NonfungiblePositionManager.deploy(uni_factory, weth9, tokenDescriptor, {"from": accounts[0]})

    # pool parameters
    price = 1.2654
    fee = FEE_LIST[1]
    tick_spacing = TICK_SPACING_LIST[1]

    print("initializing pool")
    create_pool_tx = pos_manager.createAndInitializePoolIfNecessary(
        token_a, 
        token_b, 
        fee, 
        sqrt_ratio_x96(price), 
        {"from": accounts[0]}
    )
    pool = create_pool_tx.events['PoolCreated']['pool']

    print("adding liquidity")
    # # params
    min_price = 1
    max_price = 2
    tick_lower = getTick(uni_utils, min_price, tick_spacing, floor=True)
    tick_upper = getTick(uni_utils, max_price, tick_spacing, floor=False)
    amount_0_desired = 1*1e18
    amount_1_desired = 1*1e18
    amount_0_min = 0
    amount_1_min = 0
    deadline = 10000000000000
    
    # #block_number = web3.eth.block_number
    # #block_timestamp = web3.eth.get_block(block_number).timestamp
    
    token_a.approve(pos_manager, 2**256 - 1, {'from':accounts[1]})
    token_b.approve(pos_manager, 2**256 - 1, {'from':accounts[1]})

    # for mint to work, you may have to edit v3-periphery/contracts/libraries/PoolAddress.sol:
    # bytes32 internal constant POOL_INIT_CODE_HASH = 0x67ab6764c0956bbe32399c32e0100e6e9a162929035bcf8cd5bbed5debfff967;
    # POOL_INIT_CODE_HASH = keccak256(abi.encodePacked(type(UniswapV3Pool).creationCode)); in v3-core/contracts/UniswapV3PoolDeployer.sol
    mint_pos_tx = pos_manager.mint(
        (
            token_a,
            token_b,
            fee,
            tick_lower,
            tick_upper,
            amount_0_desired,
            amount_1_desired,
            amount_0_min,
            amount_1_min,
            accounts[1],
            deadline
        ),
        {
            "from": accounts[1]
        }
    )
    pos_id, liquidity, amount0, amount1 = mint_pos_tx.return_value
    print(f"minted position {pos_id} adding {amount0/1e18} token0 and {amount1/1e18} token1")
    # print_events(mint_pos_tx)

    print("deploying router")
    swap_router = uniswap_periphery.SwapRouter.deploy(uni_factory, weth9, {"from": accounts[0]})
    
    token_a.approve(swap_router, 2**256 - 1, {'from':accounts[2]})

    print("swapping")
    amount_in = 0.1*1e18
    amount_out_min = 0
    sqrtPriceLimitX96 = 0

    swap_tx = swap_router.exactInputSingle((
        token_a, # token_in
        token_b, # token_out
        fee,
        accounts[2],
        deadline,
        amount_in,
        amount_out_min,
        sqrtPriceLimitX96
    ), {
            "from": accounts[2]
    })
    print(f"swapped {amount_in/1e18} token0 for {swap_tx.return_value/1e18} token1")

    for i in range(3):
        print(f"account {i} balance of token_a:{token_a.balanceOf(accounts[i])/1e18} token_b:{token_b.balanceOf(accounts[i])/1e18}")
        
    print(f"pool balance of token_a:{token_a.balanceOf(pool)/1e18} token_b:{token_b.balanceOf(pool)/1e18}")

    
    # description URI contains pool address, token addresses, fee tier, tokenid and image
    # description_b64 = pos_manager.tokenURI(pos_id)
    # import json
    # import base64
    # description = json.loads(base64.b64decode(description_b64.split(",")[1]))

    position = pos_manager.positions(pos_id)
    pos_tickA = position[5]
    pos_tickB = position[6]
    pos_liquidity = position[7]

    # get number of tokens in position 
    liquidity_lib = uniswap_periphery.LiquidityAmountsTest.deploy({"from": accounts[0]})
    amount0, amount1 = liquidity_lib.getAmountsForLiquidity(
        uni_utils.getPoolPrice(pool),
        uni_utils.tickToRatio(pos_tickA),
        uni_utils.tickToRatio(pos_tickB),
        pos_liquidity
    )

    print(f"position {pos_id} liquidity: {amount0/1e18} A {amount1/1e18} B")

    raise Exception