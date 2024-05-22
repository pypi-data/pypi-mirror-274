import numpy as np
cimport numpy as np
cimport cython
from cython.parallel import prange
from libc.math cimport exp
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import GridSearchCV

cdef class NWE:
    cdef double best_alpha

    cpdef np.ndarray[np.float32_t, ndim=1] run_nwe(self, np.ndarray[np.float32_t, ndim=2] indata):
        cdef np.ndarray[np.float32_t, ndim=2] X = indata
        cdef np.ndarray[np.float32_t, ndim=1] y = indata[:, 0]
        cdef np.ndarray[np.float32_t, ndim=1] y_pred

        param_grid = {'alpha': [0.5, 1.5, 2.5, 3.0, 3.5, 5.0]}
        
        # Handle sklearn operations
        kr = GridSearchCV(KernelRidge(kernel='rbf'), param_grid)
        if not hasattr(self, 'best_alpha'):
            kr.fit(X, y)
            self.best_alpha = kr.best_params_['alpha']

        cdef np.float32_t alpha = self.best_alpha
        cdef int n_samples = X.shape[0]
        cdef np.ndarray[np.float32_t, ndim=1] weights = np.empty(n_samples, dtype=np.float32)
        y_pred = np.empty(n_samples, dtype=np.float32)

        cdef double sum_weights
        cdef double sum_weighted_y
        cdef double diff
        cdef int i, j, k

        # Perform the Nadaraya-Watson prediction
        for i in range(n_samples):
            sum_weights = 0.0
            sum_weighted_y = 0.0
            for j in range(n_samples):  # Removed prange to ensure GIL is held
                diff = 0.0
                for k in range(X.shape[1]):
                    diff += (X[j, k] - X[i, k]) ** 2
                weights[j] = exp(-alpha * diff)
                sum_weights += weights[j]
                sum_weighted_y += weights[j] * y[j]
            y_pred[i] = sum_weighted_y / sum_weights

        # Optimized rolling mean
        cdef int window_size = 5
        cdef np.ndarray[np.float32_t, ndim=1] rolling_mean = np.empty(n_samples, dtype=np.float32)

        cdef double window_sum = 0.0

        for i in range(n_samples):
            window_sum += y_pred[i]
            if i >= window_size:
                window_sum -= y_pred[i - window_size]
            rolling_mean[i] = window_sum / min(i + 1, window_size)

        return rolling_mean