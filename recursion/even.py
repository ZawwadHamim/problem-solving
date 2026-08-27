def even(n):
    if n==0:
        return 0
    if n % 2 == 0:
        return n + even(n-2)
    return even(n-1)


print(even(9))