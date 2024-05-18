def fact(n):
    if n < 0:
        raise ValueError('factorial is not defined for negative numbers')
        # print('factorial is not defined for negative numbers')
    elif n == 0 or n == 1:
        return 1
    else:
        return n*fact(n-1)