cimport numpy as np
import numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)

def ewma(np.ndarray[np.float32_t, ndim=1] series, double alpha):
    cdef int n = series.shape[0]
    cdef np.ndarray[np.float32_t, ndim=1] ewma_series = np.empty(n, dtype=np.float32)
    ewma_series[0] = series[0]
    for i in range(1, n):
        ewma_series[i] = alpha * series[i] + (1 - alpha) * ewma_series[i - 1]
    return ewma_series

def ema2( np.ndarray[np.float32_t, ndim=1] source, double length):
    cdef double alpha = 2.0 / (max(1.0, length) + 1.0)
    return ewma(source, alpha)

def tema3(np.ndarray[np.float32_t, ndim=1] source, double length):
    cdef np.ndarray[np.float32_t, ndim=1] ema2_result
    cdef np.ndarray[np.float32_t, ndim=1] term1, term2, term3
    
    if isinstance(source, float):
        return source
    else:
        ema2_result = ema2(source, length)
        term1 = 3 * (ema2_result - ema2(ema2(ema2_result, length), length))
        term2 = 3 * (ema2(ema2(ema2_result, length), length) - 
                        ema2(ema2(ema2(ema2_result, length), length), length))
        term3 = ema2(ema2(ema2(ema2_result, length), length),length)
        return term1 + term2 + term3

def halftrend(np.ndarray[np.float32_t, ndim=1] high, 
                np.ndarray[np.float32_t, ndim=1] low, 
                np.ndarray[np.float32_t, ndim=1] close, 
                np.ndarray[np.float32_t, ndim=1] tr, 
                int amplitude=2, 
                double channel_deviation=2.0):
    cdef int n = high.shape[0]
    cdef np.ndarray[np.float32_t, ndim=1] atr2 = tr * 0.5
    cdef np.ndarray[np.float32_t, ndim=1] dev = channel_deviation * atr2
    cdef np.ndarray[np.float32_t, ndim=1] high_price = np.empty_like(high)
    cdef np.ndarray[np.float32_t, ndim=1] low_price = np.empty_like(low)
    cdef int i
    
    # Calculate rolling maximum and minimum with lookback
    for i in range(amplitude):
        high_price[i] = np.max(high[:i+1])
        low_price[i] = np.min(low[:i+1])
    for i in range(amplitude, n):
        high_price[i] = np.max(high[i-amplitude+1:i+1])
        low_price[i] = np.min(low[i-amplitude+1:i+1])

    cdef np.ndarray[np.float32_t, ndim=1] highma = tema3(high, amplitude*2)
    cdef np.ndarray[np.float32_t, ndim=1] lowma = tema3(low, amplitude*2)

    cdef np.ndarray[np.int32_t, ndim=1] trend = np.zeros(n, dtype=np.int32)
    cdef np.ndarray[np.int32_t, ndim=1] next_trend = np.zeros(n, dtype=np.int32)
    cdef np.ndarray[np.float32_t, ndim=1] max_low_price = np.zeros(n, dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=1] min_high_price = np.zeros(n, dtype=np.float32)

    # Initialization to prevent accessing out-of-bounds
    if n > 0:
        max_low_price[0] = low[0]
        min_high_price[0] = high[0]

    for i in range(1, n):
        if next_trend[i - 1] == 1:
            max_low_price[i] = max(low_price[i - 1], max_low_price[i - 1])

            if highma[i] < max_low_price[i] and close[i] < low[i - 1]:
                trend[i] = 1
                next_trend[i] = 0
                min_high_price[i] = high_price[i]
            else:
                trend[i] = trend[i - 1]
                next_trend[i] = next_trend[i - 1]
                min_high_price[i] = min_high_price[i - 1]
        else:
            min_high_price[i] = min(high_price[i - 1], min_high_price[i - 1])

            if lowma[i] > min_high_price[i] and close[i] > high[i - 1]:
                trend[i] = 0
                next_trend[i] = 1
                max_low_price[i] = low_price[i]
            else:
                trend[i] = trend[i - 1]
                next_trend[i] = next_trend[i - 1]
                max_low_price[i] = max_low_price[i - 1]

    cdef np.ndarray[np.float32_t, ndim=1] up = np.zeros(n, dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=1] down = np.zeros(n, dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=1] atr_high = np.zeros(n, dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=1] atr_low = np.zeros(n, dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=1] arrow_up = np.zeros(n, dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=1] arrow_down = np.zeros(n, dtype=np.float32)

    # Initialization to prevent accessing out-of-bounds
    if n > 0:
        up[0] = max_low_price[0]
        down[0] = min_high_price[0]
        atr_high[0] = tr[0]
        atr_low[0] = tr[0]

    for i in range(1, n):
        if trend[i] == 0:
            if trend[i - 1] != 0:
                up[i] = down[i - 1]
                arrow_up[i] = up[i] - atr2[i]
            else:
                up[i] = max(max_low_price[i - 1], up[i - 1])

            atr_high[i] = up[i] + dev[i]
            atr_low[i] = up[i] - dev[i]

        else:
            if trend[i - 1] != 1:
                down[i] = up[i - 1]
                arrow_down[i] = down[i] + atr2[i]
            else:
                down[i] = min(min_high_price[i - 1], down[i - 1])

            atr_high[i] = down[i] + dev[i]
            atr_low[i] = down[i] - dev[i]

    halftrend = np.where(trend == 0, up, down)
    buy = np.where((trend == 0) & (np.roll(trend, 1) == 1), 1, 0)
    sell = np.where((trend == 1) & (np.roll(trend, 1) == 0), 1, 0)

    htdf = {
        'halftrend': halftrend,
        'atrHigh': atr_high,
        'atrLow': atr_low,
        'arrowUp': arrow_up,
        'arrowDown': arrow_down,
        'buy': buy,
        'sell': sell
    }

    return htdf