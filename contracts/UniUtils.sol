// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.7.6;
pragma abicoder v2;

import '@uniswap/v3-core/contracts/libraries/TickMath.sol';
import '@uniswap/v3-core/contracts/interfaces/IUniswapV3Pool.sol';

contract UniUtils {
    function ratioToTick(uint160 sqrtPriceX96) pure public returns (int24 tick) {
        tick = TickMath.getTickAtSqrtRatio(sqrtPriceX96);
    }
    function tickToRatio(int24 tick) pure public returns (uint160 sqrtPriceX96) {
        sqrtPriceX96 = TickMath.getSqrtRatioAtTick(tick); 
    }
    function getPoolPrice(address poolAddress) view public returns (uint160 sqrtPriceX96) {
        IUniswapV3Pool pool = IUniswapV3Pool(poolAddress);
        (sqrtPriceX96, , , , , , ) = pool.slot0();
    }
}
    
    
