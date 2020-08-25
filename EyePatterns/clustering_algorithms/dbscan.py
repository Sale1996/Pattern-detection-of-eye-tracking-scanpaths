import numpy as np
from sklearn.cluster import DBSCAN
import distance


class DbScan:
    def __init__(self, eps=5, min_samples=2):
        self.eps = eps
        self.min_samples = min_samples

    def fit(self, metric, data):
        self.data = data
        X = np.arange(len(data)).reshape(-1, 1)
        dbscan_alg = DBSCAN(metric=metric, eps=self.eps, min_samples=self.min_samples)
        self.model = dbscan_alg.fit(X)

    def get_clusters(self):
        model_labels = self.model.labels_
        cluster_map = self.initialize_cluster_map_with_empty_arrays(model_labels)

        for i in range(0, len(self.data)):
            is_outlier = model_labels[i] != -1
            if is_outlier:
                cluster_map[model_labels[i]].append(self.data[i])

        return cluster_map

    def initialize_cluster_map_with_empty_arrays(self, model_labels):
        cluster_map = {}
        for i in range(0, len(model_labels)):
            cluster_map[model_labels[i]] = []
        return cluster_map


