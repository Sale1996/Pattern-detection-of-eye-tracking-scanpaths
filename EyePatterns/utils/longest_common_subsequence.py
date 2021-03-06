# Returns length of LCS for X[0..m-1], Y[0..n-1]
def longest_common_subsequence(X, Y):
    X_length = len(X)
    Y_length = len(Y)
    L = [[0 for x in range(Y_length + 1)] for x in range(X_length + 1)]

    # Following steps build L[m+1][n+1] in bottom up fashion. Note
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]
    for i in range(X_length + 1):
        for j in range(Y_length + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

                # Following code is used to print LCS
    index = L[X_length][Y_length]

    # Create a character array to store the lcs string
    lcs = [""] * (index + 1)
    lcs[index] = ""

    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = X_length
    j = Y_length
    while i > 0 and j > 0:

        # If current character in X[] and Y are same, then
        # current character is part of LCS
        if X[i - 1] == Y[j - 1]:
            lcs[index - 1] = X[i - 1]
            i -= 1
            j -= 1
            index -= 1

        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    # print("LCS of " + X + " and " + Y + " is " + "".join(lcs))
    return "".join(lcs)


# Test
X = "ACCAEF"
Y = "CCAACCF"
longest_common_subsequence(X, Y)