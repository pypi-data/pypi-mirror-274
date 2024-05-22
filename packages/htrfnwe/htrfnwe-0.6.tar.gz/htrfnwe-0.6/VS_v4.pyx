# cython: boundscheck=False, wraparound=False, nonecheck=False
import numpy as np
cimport numpy as np
from libc.math cimport fabs, isnan
from cython.parallel import prange
cimport cython

cdef class VumanchuSwing:
    
    cdef np.ndarray[double, ndim=1] ema(self, np.ndarray[double, ndim=1] x, int period):
        cdef int n = x.shape[0]
        cdef np.ndarray[double, ndim=1] weights = np.ones(period, dtype=np.float64) / period
        cdef np.ndarray[double, ndim=1] result = np.empty(n - period + 1, dtype=np.float64)
        cdef int i
        for i in range(n - period + 1):
            result[i] = np.dot(x[i:i + period], weights)
        return result

    cpdef np.ndarray[double, ndim=1] range_size(self, np.ndarray[double, ndim=1] arr, int range_period, double range_multiplier):
        cdef int n = arr.shape[0]
        cdef np.ndarray[double, ndim=1] arr_diff_abs = np.empty(n, dtype=np.float64)
        cdef np.ndarray[double, ndim=1] first_ema, second_ema, result
        cdef int i, pad_length
        
        arr_diff_abs[0] = 0
        for i in prange(1, n, nogil=True):
            arr_diff_abs[i] = fabs(arr[i] - arr[i-1])
        
        first_ema = self.ema(arr_diff_abs, range_period)
        second_ema = self.ema(first_ema, (range_period * 2) - 1)
        
        pad_length = n - second_ema.shape[0]
        result = np.empty(n, dtype=np.float64)
        result[:pad_length] = np.nan
        result[pad_length:] = second_ema * range_multiplier
        
        return result
    
    cdef double nz(self, double x):
        return 0.0 if isnan(x) else x

    cpdef np.ndarray[double, ndim=2] range_filter(self, np.ndarray[double, ndim=1] x, np.ndarray[double, ndim=1] r):
        cdef int n = x.shape[0]
        cdef np.ndarray[double, ndim=1] range_filt = np.zeros(n, dtype=np.float64)
        cdef np.ndarray[double, ndim=1] hi_band = np.zeros(n, dtype=np.float64)
        cdef np.ndarray[double, ndim=1] lo_band = np.zeros(n, dtype=np.float64)
        cdef int i
        
        range_filt[0] = x[0]
        
        for i in prange(1, n, nogil=True):
            with gil:
                range_filt[i] = self.nz(range_filt[i - 1])
            
            if not isnan(r[i]):
                if x[i] > range_filt[i - 1]:
                    range_filt[i] = max(range_filt[i - 1], x[i] - r[i])
                else:
                    range_filt[i] = min(range_filt[i - 1], x[i] + r[i])
                
            hi_band[i] = range_filt[i] + r[i]
            lo_band[i] = range_filt[i] - r[i]
        
        # Forward fill the NaNs
        for i in range(1, n):
            if isnan(range_filt[i]):
                range_filt[i] = range_filt[i - 1]
                hi_band[i] = hi_band[i - 1]
                lo_band[i] = lo_band[i - 1]
        
        return np.vstack((hi_band, lo_band, range_filt)).T

    cpdef np.ndarray[double, ndim=2] vumanchu_swing(self, np.ndarray[double, ndim=1] arr, int swing_period, double swing_multiplier):
        cdef np.ndarray[double, ndim=1] smrng = self.range_size(arr, swing_period, swing_multiplier)
        return self.range_filter(arr, smrng)