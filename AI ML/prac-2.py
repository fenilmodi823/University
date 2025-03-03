import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=100, n_features=5, n_informative=3, random_state=42)

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Original shape:", X.shape)
print("Reduced shape:", X_reduced.shape)

explained_variance = pca.explained_variance_ratio_
print("Explained Variance Ratio:", explained_variance)
print(f"Total Variance Captured: {sum(explained_variance) * 100:.2f}%")

plt.figure(figsize=(8, 6))
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='viridis', edgecolor='k', alpha=0.75)
plt.colorbar(label="Class Label")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA: Data Projection onto 2D Space")
plt.grid(True)
plt.show()
