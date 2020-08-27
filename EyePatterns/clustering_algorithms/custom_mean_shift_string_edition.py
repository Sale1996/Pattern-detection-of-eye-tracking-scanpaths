import Levenshtein
import numpy as np

from utils.e_mine import e_mine_find_common_scanpath


class MeanShiftStringEdition:
    def __init__(self, radius=2, distance_function=1):
        self.radius = radius
        if distance_function != 1:
            self.distance_between = distance_function
        else:
            self.distance_between = Levenshtein.distance

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
            unique_centroids = self.remove_duplicate_centroids_then_sort(new_centroids)
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
            new_centroid = self.find_average(in_bandwith)
            if len(new_centroid) != 0:
                new_centroids.append(new_centroid)
        return new_centroids

    def find_average(self, in_bandwith):
        return e_mine_find_common_scanpath(in_bandwith)

    def fill_in_bandiwth_with_features_in_radius(self, centroid, data):
        in_bandwith = []
        for featureset in data:
            if self.is_in_radius(featureset, centroid):
                in_bandwith.append(featureset)
        return in_bandwith

    def is_in_radius(self, featureset, centroid):
        if self.distance_between(featureset, centroid) < self.radius:
            return True
        else:
            return False

    def remove_duplicate_centroids_then_sort(self, new_centroids):
        return sorted(list(set(new_centroids)))

    def set_unique_centroids_as_final_centroids(self, uniques):
        centroids = {}
        for i in range(len(uniques)):
            centroids[i] = uniques[i]
        return centroids

    def check_if_optimized(self, centroids, prev_centroids):
        optimized = True
        for i in centroids:
            if not np.array_equal(centroids[i], prev_centroids[i]):
                optimized = False
                break
        return optimized
