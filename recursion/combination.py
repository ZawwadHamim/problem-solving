def comb(n,r):
    if n==r or r == 0:
        return 1

    return comb(n-1,r-1)+comb(n-1,r)


print(comb(5,3))