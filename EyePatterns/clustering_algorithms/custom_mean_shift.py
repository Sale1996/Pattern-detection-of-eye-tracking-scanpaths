import numpy as np


class MeanShift:
    def __init__(self, radius=2):
        self.radius = radius

    def fit(self, data):
        centroids = self.initialize_starting_centroids(data)
        self.centroids = self.make_centroids(centroids, data)

    def initialize_starting_centroids(self, data):
        centroids = {}
        for i in range(len(data)):
            centroids[i] = data[i]
        return centroids

    def make_centroids(self, centroids, data):
        while True:
            new_centroids = self.find_new_centroids(centroids, data)
            unique_centroids = self.remove_duplicate_centroids(new_centroids)
            prev_centroids = dict(centroids)
            centroids = self.set_unique_centroids_as_final_centroids(unique_centroids)
            is_optimized = self.check_if_optimized(centroids, prev_centroids)
            if is_optimized:
                break
        return centroids

    def find_new_centroids(self, centroids, data):
        new_centroids = []
        for i in centroids:
            centroid = centroids[i]
            in_bandwith = self.fill_in_bandiwth_with_features_in_radius(centroid, data)
            new_centroid = self.find_average_number(in_bandwith)
            new_centroids.append(tuple(new_centroid))
        return new_centroids

    def find_average_number(self, in_bandwith):
        return np.average(in_bandwith, axis=0)

    def fill_in_bandiwth_with_features_in_radius(self, centroid, data):
        in_bandwith = []
        for featureset in data:
            if self.is_in_radius_number(featureset, centroid):
                in_bandwith.append(featureset)
        return in_bandwith

    def is_in_radius_number(self, featureset, centroid):
        if np.linalg.norm(featureset - centroid) < self.radius:
            return True
        else:
            return False

    def remove_duplicate_centroids(self, new_centroids):
        return sorted(list(set(new_centroids)))

    def set_unique_centroids_as_final_centroids(self, uniques):
        centroids = {}
        for i in range(len(uniques)):
            centroids[i] = np.array(uniques[i])
        return centroids

    def check_if_optimized(self, centroids, prev_centroids):
        optimized = True
        # check is it optimized
        for i in centroids:
            if not np.array_equal(centroids[i], prev_centroids[i]):
                optimized = False
                break
        return optimized

