# covariance.py
import numpy as np

def generate_cov_matrix(n, structure='diagonal', block_size=None, rho=0.9):
    if structure == 'diagonal':
        return np.diag(np.full(n, (np.pi/3)**2))
    elif structure == 'block_diagonal':
        if block_size is None:
            raise ValueError("Block size must be specified for block_diagonal structure.")
        num_blocks = n // block_size
        block = np.diag(np.full(block_size, (np.pi/3)**2))
        return np.block([[block if i == j else np.zeros((block_size, block_size)) for j in range(num_blocks)] for i in range(num_blocks)])
    elif structure == 'toeplitz':
        return (np.pi/3)**2 * rho**np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    elif structure == 'ar':
        return (np.pi/3)**2 * rho**np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    else:
        raise ValueError("Invalid structure specified.")
