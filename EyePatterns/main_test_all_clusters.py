import matplotlib.pyplot as plt
import distance
from matplotlib import style
from clustering_algorithms.affinity_propagation import AffinityPropagation
from clustering_algorithms.custom_k_means import KMeans
from clustering_algorithms.custom_mean_shift import MeanShift
from clustering_algorithms.custom_mean_shift_string_edition import MeanShiftStringEdition
from clustering_algorithms.dbscan import DbScan
from prepare_data.format_sequences import format_sequences_from_student
from utils.e_mine import e_mine_find_common_scanpath
from utils.string_compare_algorithm import levenstein_sequence_similarity, is_string_similar, needleman_wunsch, \
    needleman_wunsch_with_penalty
import numpy as np


# def initialize_2D_number_data_and_plot_them():
#     number_data = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11], [8, 2], [10, 2], [9, 3]])
#     # plot data
#     plt.scatter(number_data[:, 0], number_data[:, 1])
#     plt.show()
#     return number_data
#
#
# def test_k_means_with_numbers_then_plot_results():
#     clf = KMeans(k=3)
#     clf.fit(number_data)
#
#     for centroid in clf.centroids:
#         plt.scatter(clf.centroids[centroid][0], clf.centroids[centroid][1],
#                     marker="o", color="k", s=150, linewidths=5)
#
#     for classification in clf.classifications:
#         color = colors[classification]
#         for featureset in clf.classifications[classification]:
#             plt.scatter(featureset[0], featureset[1], marker="x", color=color,
#                         s=150, linewidths=5)
#     plt.show()
#
#
# def test_mean_shift_with_numbers_then_plot_results():
#     clf_ms = MeanShift()
#     clf_ms.fit(number_data)
#     plt.scatter(number_data[:, 0], number_data[:, 1], s=150)
#     centroids = clf_ms.centroids
#     for c in centroids:
#         plt.scatter(centroids[c][0], centroids[c][1], color='k', marker="*", s=150)
#     plt.show()


def initialize_string_sequences(student_name):
    # print(format_sequences_from_student(student_name))
    return format_sequences_from_student(student_name)
    # return ["ACCAEF", "ACCEF", "AACF", "CCCEF", "CCAACCF", "CCACF"]


def print_description():
    print("***************************************************")
    print("NAME OF ALGORITHM")
    print("- *CLUSTER REPRESENTER* [CLUSTER MEMBER, CLUSTER MEMBER, CLUSTER MEMBER]")
    print("***************************************************")


def test_and_print_results_string_k_means_with_levenshtein_distance():
    kmeans_alg = KMeans(k=3, distance_function=distance.levenshtein, find_average_function=e_mine_find_common_scanpath,
                        check_is_optimized_function=is_string_similar)
    kmeans_alg.fit(string_data)
    print_k_means_results(kmeans_alg, "Levenshtein")


def test_and_print_results_string_k_means_with_needleman_wunsch_distance():
    kmeans_alg = KMeans(k=3, distance_function=needleman_wunsch, find_average_function=e_mine_find_common_scanpath,
                        check_is_optimized_function=is_string_similar)
    kmeans_alg.fit(string_data)
    print_k_means_results(kmeans_alg, "Needleman-Wunsch")


def test_and_print_results_string_k_means_with_needleman_wunsch_distance_with_extra_penalty_points():
    kmeans_alg = KMeans(k=3, distance_function=needleman_wunsch_with_penalty,
                        find_average_function=e_mine_find_common_scanpath,
                        check_is_optimized_function=is_string_similar)
    kmeans_alg.fit(string_data)
    print_k_means_results(kmeans_alg, "Needleman-Wunsch with additional penalty")


def print_k_means_results(kmeans_alg, distance_algorithm):
    centroid_cluster_map_kmeans = {}
    for i in range(0, len(kmeans_alg.centroids)):
        centroid_cluster_map_kmeans[kmeans_alg.centroids[i]] = kmeans_alg.classifications[i]
    print()
    print("K Means string edition with %s distance algorithm" % distance_algorithm)
    for centroid in centroid_cluster_map_kmeans:
        print(" - *%s* %s" % (centroid, centroid_cluster_map_kmeans[centroid]))


def test_and_print_results_string_mean_shift_with_levenshtein_distance():
    mean_shift_string_edition = MeanShiftStringEdition()
    mean_shift_string_edition.fit(string_data)

    print_mean_shift_results(mean_shift_string_edition, "Levenshtein")


def test_and_print_results_string_mean_shift_with_needleman_wunsch_distance():
    mean_shift_string_edition = MeanShiftStringEdition(distance_function=needleman_wunsch)
    mean_shift_string_edition.fit(string_data)

    print_mean_shift_results(mean_shift_string_edition, "Needleman-Wunsch")


def test_and_print_results_string_mean_shift_with_needleman_wunsch_distance_with_extra_penalty_points():
    mean_shift_string_edition = MeanShiftStringEdition(distance_function=needleman_wunsch_with_penalty)
    mean_shift_string_edition.fit(string_data)

    print_mean_shift_results(mean_shift_string_edition, "Needleman-Wunsch with additional penalty")


def print_mean_shift_results(mean_shift_string_edition, distance_algorithm):
    print()
    print("Mean Shift string edition with %s distance algorithm" % distance_algorithm)
    for centroid in mean_shift_string_edition.centroids:
        print(" - *%s*" % mean_shift_string_edition.centroids[centroid])


def test_and_print_results_string_affinity_propagation_with_levenstein_distance():
    data_as_array = np.asarray(string_data)
    lev_similarity_scores = -1 * np.array(
        [[distance.levenshtein(w1, w2) for w1 in data_as_array] for w2 in data_as_array])
    affinity_propagation_alg = AffinityPropagation()
    affinity_propagation_alg.fit(lev_similarity_scores)

    print_affinity_propagation_results(affinity_propagation_alg, data_as_array, "Levenshtein")


def test_and_print_results_string_affinity_propagation_with_needleman_wunsch_distance():
    data_as_array = np.asarray(string_data)
    lev_similarity_scores = -1 * np.array(
        [[needleman_wunsch(w1, w2) for w1 in data_as_array] for w2 in data_as_array])
    affinity_propagation_alg = AffinityPropagation()
    affinity_propagation_alg.fit(lev_similarity_scores)

    print_affinity_propagation_results(affinity_propagation_alg, data_as_array, "Needleman-Wunsch")


def test_and_print_results_string_affinity_propagation_with_needleman_wunsch_distance_with_extra_penalty_points():
    data_as_array = np.asarray(string_data)
    lev_similarity_scores = -1 * np.array(
        [[needleman_wunsch_with_penalty(w1, w2) for w1 in data_as_array] for w2 in data_as_array])
    affinity_propagation_alg = AffinityPropagation()
    affinity_propagation_alg.fit(lev_similarity_scores)

    print_affinity_propagation_results(affinity_propagation_alg, data_as_array, "Needleman-Wunsch with additional penalty")


def print_affinity_propagation_results(affinity_propagation_alg, data_as_array, distance_algorithm):
    print()
    print('Affinity Propagation with %s distance algorithm' % distance_algorithm)
    exemplar_features_map = affinity_propagation_alg.get_exemplars_and_their_features(data_as_array)
    for exemplar in exemplar_features_map:
        print(" - *%s* %s" % (exemplar, exemplar_features_map[exemplar]))


def test_and_print_results_string_db_scan_with_levenstein_distance():
    def lev_metric(x, y):
        i, j = int(x[0]), int(y[0])  # extract indices
        return distance.levenshtein(string_data[i], string_data[j])

    db_scan = DbScan()
    db_scan.fit(lev_metric, string_data)
    print_db_scan_results(db_scan, "Levenshtein")


def test_and_print_results_string_db_scan_with_needleman_wunsch_distance():
    def lev_metric(x, y):
        i, j = int(x[0]), int(y[0])  # extract indices
        return needleman_wunsch(string_data[i], string_data[j])

    db_scan = DbScan()
    db_scan.fit(lev_metric, string_data)
    print_db_scan_results(db_scan, "Needleman-Wunsch")


def test_and_print_results_string_db_scan_with_needleman_wunsch_distance_with_extra_penalty_points():
    def lev_metric(x, y):
        i, j = int(x[0]), int(y[0])  # extract indices
        return needleman_wunsch_with_penalty(string_data[i], string_data[j])

    db_scan = DbScan()
    db_scan.fit(lev_metric, string_data)
    print_db_scan_results(db_scan, "Needleman-Wunsch with additional penalty")


def print_db_scan_results(db_scan, distance_algorithm):
    print()
    print('DB Scan with %s distance algorithm' % distance_algorithm)
    for cluster in db_scan.get_clusters():
        cluster_representer = e_mine_find_common_scanpath(db_scan.get_clusters()[cluster])
        print(" - *%s* %s" % (cluster_representer, db_scan.get_clusters()[cluster]))


'''
    1# Initialize number collection and plot style
'''
# style.use('ggplot')
# number_data = initialize_2D_number_data_and_plot_them()
# colors = 10 * ["g", "r", "c", "b", "k"]

'''
    Test classification algorithms with numbers
'''
# test_k_means_with_numbers_then_plot_results()
# test_mean_shift_with_numbers_then_plot_results()

'''
    2# Initialize string collection and print description on printed form
'''
student_name = "student_1"
string_data = initialize_string_sequences(student_name)
print_description()

'''
    Test classification algorithms with strings
'''

test_and_print_results_string_k_means_with_levenshtein_distance()
test_and_print_results_string_k_means_with_needleman_wunsch_distance()
test_and_print_results_string_k_means_with_needleman_wunsch_distance_with_extra_penalty_points()

test_and_print_results_string_mean_shift_with_levenshtein_distance()
test_and_print_results_string_mean_shift_with_needleman_wunsch_distance()
test_and_print_results_string_mean_shift_with_needleman_wunsch_distance_with_extra_penalty_points()


test_and_print_results_string_affinity_propagation_with_levenstein_distance()
test_and_print_results_string_affinity_propagation_with_needleman_wunsch_distance()
test_and_print_results_string_affinity_propagation_with_needleman_wunsch_distance_with_extra_penalty_points()


test_and_print_results_string_db_scan_with_levenstein_distance()
test_and_print_results_string_db_scan_with_needleman_wunsch_distance()
test_and_print_results_string_db_scan_with_needleman_wunsch_distance_with_extra_penalty_points()