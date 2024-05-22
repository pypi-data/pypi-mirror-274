# analysis.py
import numpy as np
from itertools import combinations
import scipy.special
from gsapme.simulation import jointSim, condSim
from gsapme.models import ishigami_mod


def compute_variance_np(model, jointSim, Nv, covMat, pert=False):
    X_v = jointSim(Nv, covMat)  # Generate samples using the joint simulation function

    # Sequential execution of the model on generated samples
    Y = model(X_v)

    # Compute the variance of the model output, using ddof=1 for sample variance
    vy = np.var(Y, ddof=1)
    return vy, X_v


def conditional_elements_estimation_np(model, condSim, jointSim, No, Ni, d, vy, covMat):
    # Generate conditional samples
    condX = jointSim(No, covMat)

    # Initialize indices and combination weights
    indices = [None] * (d + 1)
    comb_weights = np.zeros(d)

    # Use NumPy to create combinations and store indices for each interaction level
    for j in range(1, d + 1):
        indices[j] = np.array(list(combinations(range(d), j))).T
        comb_weights[j-1] = 1 / scipy.special.comb(d - 1, j - 1)

    # Initialize storage for variance explained results, mirroring the structure of indices
    VEs = [None] * len(indices)

    # Estimate variance explained for each subset of variables
    for level in range(1, len(indices)):
        current_level_indices = indices[level]
        current_level_VEs = []  # Initialize an empty list to store VEs for the current level
        for subset in current_level_indices.T:
            VE = estim_VE_MC(condX, condSim, model, list(subset), Ni, vy, covMat)
            current_level_VEs.append(VE)
        VEs[level] = np.array(current_level_VEs)  # Store the VEs for the current level

    # Set the last element of VEs to 1, representing the total variance explained for the full model
    VEs[-1] = 1

    # Convert combination weights to a NumPy array for consistency
    comb_weights_array = np.array(comb_weights)

    # Return the estimated VEs, indices, and combination weights
    return VEs, indices, comb_weights_array


def estim_VE_MC(condX, condSim, model, subset, Ni, vy, covMat):
    condX = np.asarray(condX)
    No, d = condX.shape

    # Adjust subset indices to match the R function logic
    complement_subset = np.setdiff1d(np.arange(d), subset)

    varVec = np.zeros(No)
    for i in range(No):
        # Extract conditional values for each sample, ensuring xjc matches the expected shape
        xjc = condX[i, complement_subset]  # Direct indexing without further adjustment

        # Perform conditional simulation
        # Ensure the condSim function is designed to accept these parameters correctly
        X_ = condSim(Ni, subset, complement_subset, xjc, covMat)  # Adjusted order to match the function definition

        # Apply the model function
        Y_ = model(X_)
        varVec[i] = np.var(Y_, ddof=1)  # ddof=1 for sample variance

    return np.mean(varVec) / vy


def calculate_shapley_effects_np(d, indices, VEs, comb_weights):
    Shaps = np.zeros(d)
    for var_j in range(d):
        for ord in range(1, d + 1):  # Ensure ord starts from 1 for consistency with indices
            if VEs[ord] is None:
                continue

            # Correctly handle indexing to avoid deprecation warnings and errors
            idx_j = np.where(indices[ord] == var_j)[1] if ord < len(indices) else np.array([])
            idx_woj = np.where(np.all(indices[ord-1] != var_j, axis=0))[0] if ord-1 > 0 else np.array([])

            # Adjust effect calculation using np.take, ensuring indices are valid
            effect_incl_j = np.sum(np.take(VEs[ord], idx_j, axis=0)) if idx_j.size > 0 else 0
            effect_excl_j = np.sum(np.take(VEs[ord-1], idx_woj, axis=0)) if idx_woj.size > 0 else 0

            # Compute the total incremental effect and update Shapley values
            Shaps[var_j] += comb_weights[ord-1] * (effect_incl_j - effect_excl_j) if ord-1 < len(comb_weights) else 0

    Shaps /= d
    return Shaps


def identify_zero_players_np(indices, VEs, tol=None):
    """
    Identifies inputs with zero or negligible total Sobol indices (zero players) using a numpy-centric approach.

    Parameters:
    - indices: A list of numpy arrays, where each array represents a set of input indices for each order of interaction.
    - VEs: A list where each element is a numpy array representing variance explained (VEs) for each set of inputs.
           Elements of VEs are converted to numpy arrays if not already.
    - tol: A tolerance level below which variance contributions are considered negligible. If None, exact zeros are considered.

    Returns:
    - A numpy array of input indices considered as zero players, adjusted for 0-based indexing.
    """
    # Convert the first element of VEs to a numpy array if it's not already one
    VEs_1 = np.asarray(VEs[1])

    # Perform the comparison with tol
    if tol is not None:
        idx_z = np.where(VEs_1 <= tol)[0]
    else:
        idx_z = np.where(VEs_1 == 0)[0]

    return idx_z


def find_zero_coalitions_np(VEs, tol=0.1):
    """
    Identifies coalitions of inputs with zero or negligible variance contributions.

    Parameters:
    - VEs: A list of numpy arrays where each array represents variance explained (VEs)
           for each set of inputs at different interaction orders. The first element can be None.
    - tol: A tolerance level below which variance contributions are considered negligible.
           If tol is None, exact zeros are considered.

    Returns:
    - A numpy array of indices representing the orders of coalitions with zero or negligible
      variance contributions, adjusted for Python's 0-based indexing.
    """
    Z_coal_order = []

    # Iterate over each set of variance effects, starting from the first element
    for i, ve in enumerate(VEs):
        if ve is not None:  # Skip None elements
            # Check if any variance contributions meet the specified criteria
            if tol is None:
                zero_criteria_met = np.any(ve == 0)
            else:
                zero_criteria_met = np.any(ve <= tol)

            # If the criteria are met, append the index (adjusted for 0-based indexing in Python)
            if zero_criteria_met:
                Z_coal_order.append(i)

    return np.array(Z_coal_order, dtype=int)



def recur_PV(indices, VEs):
    """
    Recursively calculates the partial variances (Ps) for each order of input interaction.
    """
    d = len(indices) - 1
    Ps = [None] * (d + 1)  # Adjust for Python indexing

    # Assign first order effects directly from VEs
    Ps[1] = np.atleast_1d(VEs[1])

    for ord in range(2, d + 1):
        if ord < len(VEs) and VEs[ord] is not None:
            Ws = np.atleast_1d(VEs[ord])
            if Ws.size == 0:  # Check if Ws is empty
                continue  # Skip to the next iteration if Ws has no elements
            Ps[ord] = np.zeros(Ws.size)

            for i in range(Ws.size):
                S = np.array(indices[ord])[:, i] if indices[ord].shape[1] > i else np.array([])

                idx_Spi = []
                for j in range(indices[ord - 1].shape[1]):
                    if np.all(np.isin(S[:-1], indices[ord - 1][:, j])):
                        idx_Spi.append(j)

                if not idx_Spi:
                    Ps[ord][i] = 0  # Assign 0 if no matching subsets are found
                else:
                    denom = np.sum(1 / Ps[ord - 1][idx_Spi])
                    Ps[ord][i] = Ws[i] / denom if denom != 0 else 0

    # Remove None values and ensure all elements are numpy arrays
    Ps = [p for p in Ps if p is not None]

    return Ps




def calculate_pme_zero_players(d, indices, VEs, tol, idx_z, Z_coal_order):
    Z_cardMax = max(Z_coal_order) - 1

    # Identifying specific coalitions
    Z_coal_cardMax = []
    for i, ve in enumerate(VEs[Z_cardMax + 1]):
        if (tol is None and ve == 0) or (tol is not None and ve <= tol):
            Z_coal_cardMax.append(indices[Z_cardMax + 1][:, i])
    Z_coal_cardMax = np.array(Z_coal_cardMax).T if Z_coal_cardMax else np.array([])

    PS_i = np.zeros(d)
    PS_N = np.zeros(d)

    # Adjusted loop to avoid 'IndexError'
    for idx_Zcoal in range(Z_coal_cardMax.shape[1] if Z_coal_cardMax.ndim > 1 else (1 if Z_coal_cardMax.size > 0 else 0)):
        Z_coal = Z_coal_cardMax[:, idx_Zcoal] if Z_coal_cardMax.ndim > 1 else Z_coal_cardMax

        # Preparation of indices_ and VEs_ for recursive calculation
        indices_ = [np.array([]) for _ in range(d - Z_cardMax + 1)]
        VEs_ = [np.array([]) for _ in range(d - Z_cardMax + 1)]

        # Populate these structures based on the current coalition
        for i in range(d - Z_cardMax):
            if i + 1 < len(indices):
                check_mask = np.isin(indices[i + 1], Z_coal)
                idx_ind_null = np.where(np.sum(check_mask, axis=0) == 0)[0]
                if idx_ind_null.size > 0:
                    ind_tmp = indices[i + 1][:, idx_ind_null]
                    Z_coal_rep = np.tile(Z_coal, (ind_tmp.shape[1], 1)).T
                    indices_[i + 1] = np.concatenate((ind_tmp, Z_coal_rep), axis=0)

        for i in range(len(indices_) - 1):
            if indices_[i + 1].size > 0:
                idx_get = []
                for col in range(indices_[i + 1].shape[1]):
                    column = indices_[i + 1][:, col]
                    match_mask = np.all(np.isin(indices[Z_cardMax + i + 1], column), axis=0)
                    idx_get.extend(np.where(match_mask)[0])
                if idx_get:
                    VEs_[i + 1] = VEs[Z_cardMax + i + 1][idx_get]

        PS = recur_PV(indices_, VEs_)  # Adjusted to pass the correct parameters

        # Process each order's partial variances from PS
        for ord, P in enumerate(PS, start=1):
            if ord == 1:
                continue  # Skip the first order, assuming it's handled separately or not relevant for the update
            if P.size > 0:
                # Example update logic, assuming idx_z corresponds to indices to be updated in PS_i
                # This needs to be adjusted based on your specific logic for applying PS to PS_i and PS_N
                PS_i += P  # This is a placeholder operation. You'll need to adjust it to match your intended calculation.
                PS_N += 1 / np.sum(P)  # Adjust as necessary for your logic

    # Final calculations and return statement
    PS_N_safe = np.where(PS_N == 0, 1, PS_N)  # Avoid division by zero
    PV = PS_i / PS_N_safe
    PV = PV.reshape(-1, 1)

    return PV


def calculatePME(d, indices, VEs, tol):
    # Assuming identify_zero_players and find_zero_coalitions are defined elsewhere
    idx_z = identify_zero_players_np(indices, VEs, tol)
    Z_coal_order = find_zero_coalitions_np(VEs, tol)

    # Check if idx_z contains any elements
    if any(idx_z):
        # Assuming calculate_pme_zero_players is defined as per previous discussions
        return calculate_pme_zero_players(d, indices, VEs, tol, idx_z, Z_coal_order)
    else:
        # Assuming recur_PV is defined and adapted from your recur.PV
        PS = recur_PV(indices, VEs)

        # Adaptation of R's matrix(rev(PS[[d]] / PS[[d - 1]]), ncol = 1)
        # Assuming PS is a list of arrays where each array corresponds to an order of interaction
        # and you want to reverse the division result of the last two orders' variances
        last_order_ratio = PS[-1] / PS[-2]
        return last_order_ratio[::-1].reshape(-1, 1)  # Reverse and reshape for column vector



if __name__=="__main__":
    #cov_mat = generate_cov_matrix(4, structure='diagonal')
    Nv = 100  # Number of samples for variance estimation
    No = 20  # Number of samples for conditional expectation
    Ni = 200 # Number of inner loop samples for Monte Carlo estimation
    tol = 0.2  # Tolerance for identifying zero players
    pert = False  # Whether to perturb the jointSim function

    covMat = np.array([[np.power(np.pi/3, 2), 0, 0, 0],
                    [0, np.power(np.pi/3, 2), 0, 0],
                    [0, 0, np.power(np.pi/3, 2), 0],
                    [0, 0, 0, np.power(np.pi/3, 2)]])

    # Compute the variance
    vy, X_v = compute_variance_np(ishigami_mod, jointSim, Nv, covMat=covMat, pert=False)
    d = X_v.shape[1]

    VEs, indices, comb_weights = conditional_elements_estimation_np(
        model=ishigami_mod,
        condSim=condSim,
        jointSim=jointSim,
        No=No,
        Ni=Ni,
        d=d,
        vy=vy,
        covMat=covMat
    )


    print(VEs)
    print(indices)

    print(calculate_shapley_effects_np(d, indices, VEs, comb_weights))
    
    print(calculatePME(d, indices, VEs, tol))