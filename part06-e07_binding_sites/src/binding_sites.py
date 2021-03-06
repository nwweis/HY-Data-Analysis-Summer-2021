#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import accuracy_score
from sklearn.metrics import pairwise_distances

from matplotlib import pyplot as plt

import seaborn as sns
sns.set(color_codes=True)
import scipy
import scipy.spatial as sp
import scipy.cluster.hierarchy as hc

def find_permutation(n_clusters, real_labels, labels):
    permutation=[]
    for i in range(n_clusters):
        idx = labels == i
        # Choose the most common label among data points in the cluster
        new_label=scipy.stats.mode(real_labels[idx])[0][0]
        permutation.append(new_label)
    return permutation

def toint(x):
    nuc2int = {'A':0, 'C':1, 'G':2, 'T':3}
    return nuc2int.get(x)

def get_features_and_labels(filename):
    df = pd.read_csv(filename, sep='\t')
    df['split'] = [list(x) for x in df['X']]
    X = [[toint(y) for y in x] for x in df['split']]

    return (np.array(X), df.y)

def plot(distances, method='average', affinity='euclidean'):
    mylinkage = hc.linkage(sp.distance.squareform(distances), method=method)
    g=sns.clustermap(distances, row_linkage=mylinkage, col_linkage=mylinkage )
    g.fig.suptitle(f"Hierarchical clustering using {method} linkage and {affinity} affinity")
    plt.show()

def cluster_euclidean(filename):
    X, y = get_features_and_labels(filename)
    clustering = AgglomerativeClustering(linkage='average', affinity='euclidean').fit(X)
    permutation = find_permutation(2, y, clustering.labels_)
    # pD = pairwise_distances(X, metric="euclidean")
    # plot(pD, "average", "euclidean")
    return accuracy_score(y, [permutation[label] for label in clustering.labels_])

def cluster_hamming(filename):
    X, y = get_features_and_labels(filename)
    pD = pairwise_distances(X, metric = "hamming")
    clustering = AgglomerativeClustering(linkage='average', affinity='precomputed').fit(pD)
    permutation = find_permutation(2, y, clustering.labels_)
    # plot(pD, "average", "hamming")
    return accuracy_score(y, [permutation[label] for label in clustering.labels_])


def main():
    print("Accuracy score with Euclidean affinity is", cluster_euclidean("src/data.seq"))
    print("Accuracy score with Hamming affinity is", cluster_hamming("src/data.seq"))

if __name__ == "__main__":
    main()
