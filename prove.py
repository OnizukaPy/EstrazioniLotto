from itertools import combinations, permutations, combinations_with_replacement

numeri = [1, 2, 3]
comb = list(combinations(numeri, 2))
print(comb)

comb = list(permutations(numeri, 2))
print(comb)

comb = list(combinations_with_replacement(numeri, 2))
print(comb)

a = 1
print(len(a))