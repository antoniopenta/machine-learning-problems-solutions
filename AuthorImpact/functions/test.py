#utility used to check if two lists are equal
def checkEqual(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)