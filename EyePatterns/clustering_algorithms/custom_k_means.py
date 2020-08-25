import numpy as np
from random import seed
from random import randint


class KMeans:
    def __init__(self, k=2, tol=0.0001, max_iter=300, seed_in=1, distance_function=1, find_average_function=1,
                 check_is_optimized_function=1):
        self.k = k
        self.tol = tol
        self.max_iter = max_iter
        self.centroids = {}
        self.classifications = {}
        self.seed_in = seed_in
        if distance_function != 1:
            self.distance_between = distance_function
        else:
            self.distance_between = self.euclidean_distance
        if find_average_function != 1:
            self.find_average_feature = find_average_function
        else:
            self.find_average_feature = self.find_average_number
        if check_is_optimized_function != 1:
            self.is_optimized = check_is_optimized_function
        else:
            self.is_optimized = self.is_optimized_number

    def fit(self, data):
        seed(self.seed_in)

        self.assign_starting_centroids(data)

        for i in range(self.max_iter):
            self.assign_classifications_map()
            self.classify_data(data)
            # save values of previous centroids
            prev_centroids = dict(self.centroids)
            # setting new values to centroids
            self.move_centroids()

            is_found_nan_centroid = self.isThereNaNCentroid(data)

            if is_found_nan_centroid:
                self.assign_starting_centroids(data)
                continue

            optimized = self.check_if_optimized(prev_centroids)

            if optimized:
                break

    def predict(self, data):
        distances = self.calculate_distance_function(data)
        classification = distances.index(min(distances))
        return classification

    def assign_starting_centroids(self, data):
        self.centroids = {}
        pickedIndexes = {}
        i = 0
        while True:
            indexOfTheNextData = randint(0, len(data) - 1)
            if indexOfTheNextData not in pickedIndexes:
                self.centroids[i] = data[indexOfTheNextData]
                i = i + 1
                if i == self.k:
                    break

    def assign_classifications_map(self):
        self.classifications = {}
        for i in range(self.k):
            self.classifications[i] = []

    def classify_data(self, data):
        for featureset in data:
            distances = self.calculate_distance_function(featureset)
            classification = distances.index(min(distances))
            self.classifications[classification].append(featureset)

    def calculate_distance_function(self, featureset):
        return [self.distance_between(featureset, self.centroids[centroid]) for centroid in self.centroids]

    def move_centroids(self):
        for classification in self.classifications:
            if len(self.classifications[classification]) > 0:
                # TODO: napraviti da korisnik ubacuje svoju average funkciju, nama moze biti npr onaj eMINE algoritam
                self.centroids[classification] = self.find_average_feature(self.classifications[classification])
            else:
                self.centroids[classification] = []

    def isThereNaNCentroid(self, data):
        for centroid in self.centroids:
            if len(self.centroids[centroid]) < 1:
                return True

        return False

    def check_if_optimized(self, prev_centroids):
        optimized = True
        for c in self.centroids:
            original_centroid = prev_centroids[c]
            current_centroid = self.centroids[c]
            if self.is_optimized(current_centroid, original_centroid):
                optimized = False
        return optimized

    # Default functions addressed to numbers
    def find_average_number(self, classifications):
        return np.average(classifications, axis=0)

    def euclidean_distance(self, x, y):
        return np.linalg.norm(x - y)

    def is_optimized_number(self, current_centroid, original_centroid):
        if np.sum((current_centroid - original_centroid) / original_centroid * 100.0) > self.tol:
            return True
        else:
            return False
