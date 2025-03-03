import numpy as np
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

X_sparse = csr_matrix([
    [2, 7, 8, 2, 1],
    [3, 6, 4, 5, 8],
    [6, 8, 0, 4, 2],
    [3, 2, 7, 3, 9],
    [5, 1, 3, 8, 6]
])

n_components = min(X_sparse.shape) - 1
svd = TruncatedSVD(n_components=n_components, random_state=42)

X_reduced = svd.fit_transform(X_sparse)

print("Reduced Data Matrix (First 2 Components):")
print(np.round(X_reduced, 4))

print("\nOriginal shape:", X_sparse.shape)
print("Reduced shape:", X_reduced.shape)

explained_variance = svd.explained_variance_ratio_
print("\nExplained variance by each component:")
print(np.round(explained_variance, 4))

print("\nTotal variance retained:", round(sum(explained_variance) * 100, 2), "%")
