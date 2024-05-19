def fact(n):
    """
    Tính giai thừa của một số nguyên dương n.

    Tham số:
    - n: số dương

    Trả về:
    - Giai thừa của n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n==0 or n==1:
        return 1
    else:  
        return n * fact(n-1)
