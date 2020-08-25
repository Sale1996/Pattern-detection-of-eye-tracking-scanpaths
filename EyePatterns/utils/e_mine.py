from utils.longest_common_subsequence import longest_common_subsequence
from utils.string_compare_algorithm import levenstein_string_similarity


def e_mine_find_common_scanpath(scanpath_list):
    if len(scanpath_list) == 0:
        return []

    if len(scanpath_list) == 1:
        return scanpath_list[0]

    while len(scanpath_list) != 1:
        indexes_of_most_similar_scanpaths = find_indexes_of_most_similar_scan_paths(scanpath_list)

        common_scanpath = find_the_common_scan_path(indexes_of_most_similar_scanpaths[0],
                                                    indexes_of_most_similar_scanpaths[1], scanpath_list)
        scanpath_list = remove_similar_scanpaths_from_list(indexes_of_most_similar_scanpaths[0],
                                                           indexes_of_most_similar_scanpaths[1], scanpath_list)
        scanpath_list.append(common_scanpath)

    return scanpath_list[0]


def find_indexes_of_most_similar_scan_paths(scanpath_list):
    best_similarity_score = -1
    indexes_of_most_similar_scanpaths = []
    for i in range(0, len(scanpath_list)):
        for j in range(i + 1, len(scanpath_list)):
            distance = levenstein_string_similarity(scanpath_list[i], scanpath_list[j])
            if best_similarity_score == -1 or distance < best_similarity_score:
                best_similarity_score = distance
                indexes_of_most_similar_scanpaths = [i, j]
    return indexes_of_most_similar_scanpaths


def find_the_common_scan_path(i, j, scanpath_list):
    common_scanpath = longest_common_subsequence(scanpath_list[i], scanpath_list[j])
    return common_scanpath


def remove_similar_scanpaths_from_list(i, j, scanpath_list):
    return [e for e in scanpath_list if e not in (scanpath_list[i], scanpath_list[j])]


# # Test
#
# string_data = ["ACCAEF", "ACCEF", "AACF", "CCCEF", "CCAACCF", "CCACF"]
#
# print(e_mine_find_common_scanpath(string_data))
