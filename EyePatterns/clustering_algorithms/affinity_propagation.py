# from work  L Frey, Brendan J., and Delbert Dueck. "Clustering by passing messages between data points." science 315.5814 (2007): 972-976
# https://science.sciencemag.org/content/315/5814/972
import numpy as np
import sklearn.cluster


class AffinityPropagation:
    def __init__(self, affinity='precomputed', damping=0.5):
        self.affinity = affinity
        self.damping = damping

    def fit(self, similarity_scores):
        self.aff_prop = sklearn.cluster.AffinityPropagation(affinity=self.affinity, damping=self.damping)
        self.aff_prop.fit(similarity_scores)

    def get_exemplars_and_their_features(self, data):
        exemplar_features_map = {}
        for cluster_id in np.unique(self.aff_prop.labels_):
            exemplar = data[self.aff_prop.cluster_centers_indices_[cluster_id]]
            cluster = np.unique(data[np.nonzero(self.aff_prop.labels_ == cluster_id)])
            exemplar_features_map[exemplar] = cluster
        return exemplar_features_map


