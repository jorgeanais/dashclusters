"""
This script perform different clustering algorithms to a random data set.
Results are stored in a pandas dataframe.

Code based on the example available at:
https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html
"""

import time
import warnings

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

import pandas as pd


n_samples = 2500
X, y = datasets.make_blobs(
    n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=170
)

# Create pandas dataframe
df = pd.DataFrame(X, columns=["x0", "x1"])
df["y"] = y

params = {
    "quantile": 0.3,
    "eps": 0.18,
    "damping": 0.9,
    "preference": -200,
    "n_neighbors": 2,
    "n_clusters": 3,
    "min_samples": 5,
    "xi": 0.035,
    "min_cluster_size": 0.2,
}

# normalize dataset for easier parameter selection
X = StandardScaler().fit_transform(X)

# Update dataframe
df = pd.concat([df, pd.DataFrame(X, columns=["x0_s", "x1_s"])], axis=1)

# estimate bandwidth for mean shift
bandwidth = cluster.estimate_bandwidth(X, quantile=params["quantile"])

# connectivity matrix for structured Ward
connectivity = kneighbors_graph(
    X, n_neighbors=params["n_neighbors"], include_self=False
)
# make connectivity symmetric
connectivity = 0.5 * (connectivity + connectivity.T)

# ============
# Create cluster objects
# ============
ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
two_means = cluster.MiniBatchKMeans(n_clusters=params["n_clusters"])
ward = cluster.AgglomerativeClustering(
    n_clusters=params["n_clusters"], linkage="ward", connectivity=connectivity
)
spectral = cluster.SpectralClustering(
    n_clusters=params["n_clusters"],
    eigen_solver="arpack",
    affinity="nearest_neighbors",
)
dbscan = cluster.DBSCAN(eps=params["eps"])
optics = cluster.OPTICS(
    min_samples=params["min_samples"],
    xi=params["xi"],
    min_cluster_size=params["min_cluster_size"],
)
affinity_propagation = cluster.AffinityPropagation(
    damping=params["damping"], preference=params["preference"], random_state=0
)
average_linkage = cluster.AgglomerativeClustering(
    linkage="average",
    affinity="cityblock",
    n_clusters=params["n_clusters"],
    connectivity=connectivity,
)
birch = cluster.Birch(n_clusters=params["n_clusters"])
gmm = mixture.GaussianMixture(n_components=params["n_clusters"], covariance_type="full")

clustering_algorithms = (
    ("MiniBatch KMeans", two_means),
    ("Affinity Propagation", affinity_propagation),
    ("MeanShift", ms),
    ("Spectral Clustering", spectral),
    ("Ward", ward),
    ("Agglomerative Clustering", average_linkage),
    ("DBSCAN", dbscan),
    ("OPTICS", optics),
    ("BIRCH", birch),
    ("Gaussian\nMixture", gmm),
)


for name, algorithm in clustering_algorithms:
    t0 = time.time()

    # catch warnings related to kneighbors_graph
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="the number of connected components of the "
            + "connectivity matrix is [0-9]{1,2}"
            + " > 1. Completing it to avoid stopping the tree early.",
            category=UserWarning,
        )
        warnings.filterwarnings(
            "ignore",
            message="Graph is not fully connected, spectral embedding"
            + " may not work as expected.",
            category=UserWarning,
        )
        algorithm.fit(X)

    t1 = time.time()
    if hasattr(algorithm, "labels_"):
        y_pred = algorithm.labels_.astype(int)
    else:
        y_pred = algorithm.predict(X)

    df[name] = y_pred

# Labels to str
df.to_csv("data/clustering_data.csv")
