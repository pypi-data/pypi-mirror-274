# simulation.py
import numpy as np
import pandas as pd
from .covariance import generate_cov_matrix

def jointSim(n, covMat):
    # Simulate n samples from a multivariate normal distribution
    return np.random.multivariate_normal(mean=np.zeros(4), cov=covMat, size=n)


def conditional_mvn(mean, cov, known_indices, known_values):
    def compute_conditional(mean, cov, known_indices, known_values):
        # Ensure known_values is 1-dimensional for subtraction
        known_values = np.array(known_values).reshape(-1)

        if len(known_indices) == len(mean):
            return known_values
        elif len(known_indices) == 0:
            return np.random.multivariate_normal(mean=mean, cov=cov, size=1).flatten()

        unknown_indices = np.setdiff1d(np.arange(len(mean)), known_indices)
        sigma_known_known = cov[np.ix_(known_indices, known_indices)]
        sigma_known_unknown = cov[np.ix_(known_indices, unknown_indices)]
        sigma_unknown_known = cov[np.ix_(unknown_indices, known_indices)]
        sigma_unknown_unknown = cov[np.ix_(unknown_indices, unknown_indices)]

        mu_known = mean[known_indices]
        mu_unknown = mean[unknown_indices]

        # Reshape known_values - mu_known to ensure it's a column vector for matrix multiplication
        diff = (known_values - mu_known).reshape(-1, 1)

        mu_cond = mu_unknown + np.dot(sigma_unknown_known, np.linalg.inv(sigma_known_known)).dot(diff).flatten()
        sigma_cond = sigma_unknown_unknown - np.dot(sigma_unknown_known, np.linalg.inv(sigma_known_known)).dot(sigma_known_unknown)

        return np.random.multivariate_normal(mu_cond, sigma_cond)

    return compute_conditional(mean, cov, known_indices, known_values)


def condSim(n, Sj, Sjc, xjc, covMat):
    import numpy as np
    import pandas as pd

    d = len(covMat)
    mean_vector = np.zeros(d)
    df_samples = pd.DataFrame(index=np.arange(n), columns=np.arange(d))

    for i in range(n):
        if len(Sjc) == d:
            df_samples.iloc[i, :] = xjc
        elif len(Sjc) > 0:
            xjc_array = np.array(xjc)
            simulated_values = conditional_mvn(mean_vector, covMat, Sjc, xjc_array)
            df_samples.iloc[i, Sjc] = xjc_array  # Assign known values
            if len(Sj) > 0:
                df_samples.iloc[i, Sj] = simulated_values  # Fill simulated values for Sj
        else:
            df_samples.iloc[i, :] = np.random.multivariate_normal(mean_vector, covMat)

    # Convert the DataFrame to a 2-D NumPy array
    numpy_array = df_samples.to_numpy()

    # Convert the NumPy array to a 2D list
    output_list = numpy_array.tolist()

    return output_list

