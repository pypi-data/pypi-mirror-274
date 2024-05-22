# models.py
import numpy as np
import pandas as pd

def ishigami_mod(X):
    """
    Calculate the Ishigami function for a given set of inputs.

    Parameters:
    - X: A DataFrame or 2D array where each row is a set of inputs (X1, X2, X3, ...).
         Only the first three columns are used in the computation.

    Returns:
    - Y: The output of the Ishigami function for each input set.
    """
    # Ensure X is a DataFrame for easy columnwise operations
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    # Apply the Ishigami function component-wise
    Y1 = np.sin(X.iloc[:, 0])
    Y2 = 7 * np.sin(X.iloc[:, 1])**2 if X.shape[1] >= 2 else 0
    Y3 = 0.1 * X.iloc[:, 2]**4 * np.sin(X.iloc[:, 0]) if X.shape[1] >= 3 else 0
    Y = Y1 + Y2 + Y3

    return Y


def borehole_function(X):
    """
    Calculate the borehole function for a given set of inputs.

    Parameters:
    - X: A DataFrame or 2D array where each row is a set of inputs (rw, r, Tu, Hu, Tl, Hl, L, Kw).
         Each parameter corresponds to a physical property affecting the water flow through a borehole.

    Returns:
    - Q: The output flow rate through the borehole for each input set.
    """
    # Ensure X is a DataFrame for easy columnwise operations
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X, columns=['rw', 'r', 'Tu', 'Hu', 'Tl', 'Hl', 'L', 'Kw'])

    # Apply the Borehole function formula
    log_term = np.log(X['r'] / X['rw'])
    Q = (2 * np.pi * X['Tu'] * (X['Hu'] - X['Hl'])) / (
        log_term * (1 + (2 * X['L'] * X['Tu']) / (log_term * X['rw']**2 * X['Kw']) + X['Tu'] / X['Tl'])
    )

    return Q


def hundred_d_function(X):
    d = X.shape[1]
    indices = np.arange(1, d + 1)
    term1 = -5 / d * np.sum(indices * X, axis=1)
    term2 = 1 / d * np.sum(indices * X**3, axis=1)
    term3 = 1 / (3 * d) * np.sum(indices * np.log(X**2 + X**4), axis=1)
    interactions = X[:, 0]*X[:, 1]**2 + X[:, 1]*X[:, 3] - X[:, 2]*X[:, 4] + X[:, 50] + X[:, 49]*X[:, 53]**2
    return 3 + term1 + term2 + term3 + interactions