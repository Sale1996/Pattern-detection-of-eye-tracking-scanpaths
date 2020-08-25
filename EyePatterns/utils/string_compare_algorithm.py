def is_string_similar(string1, string2):
    if levenstein_sequence_similarity(string1, string2) >= 0.8:
        return True
    else:
        return False


# Compare similarity between two strings using levenstein algorithm (https://pypi.org/project/python-Levenshtein/0.12.0/)
def levenstein_string_similarity(string1, string2):
    import Levenshtein

    return Levenshtein.distance(string1, string2)


# Compare similarity between two string seqences using levenstein package
def levenstein_sequence_similarity(sequence1, sequence2):
    import Levenshtein

    return Levenshtein.setratio(sequence1, sequence2)


delta = lambda x, y, i, j: 1 if x[i] != y[j] else 0


def needleman_wunsch(x, y):
    m = len(x)
    n = len(y)

    OPT = instantiate_matrix_with_zeros(m, n)

    OPT = fill_edges_with_penalty_points(OPT, m, n)

    for j in range(1, n + 1):
        # kaze sada iterira svaki red od leva na desno i za svaku kolonu posebno
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # i je row , j je column
                # take MIN of: align, delete, insert
                OPT[i][j] = min(OPT[i - 1][j - 1] + delta(x, y, i - 1, j - 1),
                                OPT[i - 1][j] + 1,
                                OPT[i][j - 1] + 1)

    # for line in OPT:
    #     print(line)

    return OPT[m][n]


def needleman_wunsch_with_penalty(x, y):
    m = len(x)
    n = len(y)

    OPT = instantiate_matrix_with_zeros(m, n)

    OPT = fill_edges_with_penalty_points(OPT, m, n)

    for j in range(1, n + 1):
        # kaze sada iterira svaki red od leva na desno i za svaku kolonu posebno
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # i je row , j je column
                # take MIN of: align, delete, insert
                OPT[i][j] = min(OPT[i - 1][j - 1] + delta(x, y, i - 1, j - 1) + extraPenaltyChange(x, y, i - 1, j - 1),
                                OPT[i - 1][j] + 1 + extraPenaltyDeleteInsert(y, j - 1),
                                OPT[i][j - 1] + 1 + extraPenaltyDeleteInsert(x, i - 1))

    # for line in OPT:
    #     print(line)

    return OPT[m][n]


def extraPenaltyChange(x, y, i, j):
    needleman_wunsch_penalty_map = {
        'AA': 0,
        'AB': 0.5,
        'AC': 1,
        'AD': 1.5,
        'AE': 2,
        'AF': 2.5,
        'AG': 2,
        'AH': 2.5,
        'BB': 0,
        'BC': 1.5,
        'BD': 1,
        'BE': 2.5,
        'BF': 2,
        'BG': 2.5,
        'BH': 2,
        'CC': 0,
        'CD': 0.5,
        'CE': 1,
        'CF': 1.5,
        'CG': 1,
        'CH': 1.5,
        'DD': 0,
        'DE': 1.5,
        'DF': 1,
        'DG': 1.5,
        'DH': 1,
        'EE': 0,
        'EF': 0.5,
        'EG': 2,
        'EH': 2.5,
        'FF': 0,
        'FG': 2.5,
        'FH': 2,
        'GG': 0,
        'GH': 0.5,
        'HH': 0
    }

    if x[i] != y[j]:
        if '' + x[i] + y[j] in needleman_wunsch_penalty_map:
            return needleman_wunsch_penalty_map['' + x[i] + y[j]]
        else:
            return needleman_wunsch_penalty_map['' + y[j] + x[i]]
    else:
        return 0


def extraPenaltyDeleteInsert(data, index):
    characters_that_represents_long_look = ['B', 'D', 'F', 'H']
    if data[index] in characters_that_represents_long_look:
        return 1
    else:
        return 0


# ivice se samo sabiraju, po pravilu
def fill_edges_with_penalty_points(OPT, m, n):
    for i in range(1, m + 1):
        OPT[i][0] = i
    for j in range(1, n + 1):
        OPT[0][j] = j

    return OPT


def instantiate_matrix_with_zeros(m, n):
    OPT = [[0 for i in range(n + 1)] for j in range(m + 1)]
    return OPT

# string_data = ["ACCAEF", "ACCEF", "AACF", "CCCEF", "CCAACCF", "CCACF"]
#
# print(string_data[1], string_data[2])
# print(levenstein_string_similarity(string_data[1], string_data[2]))
# print(levenstein_sequence_similarity(string_data[1], string_data[2]))
#
# print(string_data[1], string_data[1])
# print(levenstein_string_similarity(string_data[1], string_data[1]))
# print(levenstein_sequence_similarity(string_data[1], string_data[1]))
#
# print(needleman_wunsch(string_data[1], string_data[2]))
# print(needleman_wunsch('TGACGTGC', 'TCGACGTCA'))
