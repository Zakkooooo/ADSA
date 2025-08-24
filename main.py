def school_add(I1: str, I2: str, B: int) -> str:
    # Pad to equal length
    n = max(len(I1), len(I2))
    I1 = I1.zfill(n)
    I2 = I2.zfill(n)

    carry = 0
    result = []

    # Add from right to left
    for i in range(n - 1, -1, -1):
        d1 = ord(I1[i]) - ord('0')
        d2 = ord(I2[i]) - ord('0')
        total = d1 + d2 + carry
        result.append(str(total % B))
        carry = total // B

    if carry > 0:
        result.append(str(carry))

    result.reverse()
    return ''.join(result).lstrip("0") or "0"

def subtraction(a: str, b: str, base: int) -> str:
    # Assumes a >= b
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)

    result = []
    borrow = 0
    for i in range(n - 1, -1, -1):
        da = (ord(a[i]) - ord('0')) - borrow
        db = (ord(b[i]) - ord('0'))
        if da < db:
            da += base
            borrow = 1
        else:
            borrow = 0
        result.append(str(da - db))

    result.reverse()
    return ''.join(result).lstrip("0") or "0"

def multiply(num1: str, num2: str, base: int) -> str:
    n = len(num1)
    m = len(num2)
    result = [0] * (n + m)

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
            sum_val = mul + result[i + j + 1]
            result[i + j + 1] = sum_val % base
            result[i + j] += sum_val // base

    # build string
    k = 0
    while k < len(result) and result[k] == 0:
        k += 1
    return ''.join(str(d) for d in result[k:]) or "0"

def karatsuba(a: str, b: str, base: int) -> str:
    len1, len2 = len(a), len(b)
    if len1 < 4 or len2 < 4:
        return multiply(a, b, base)

    n = max(len1, len2)
    p = 1
    while p < n:
        p <<= 1
    n = p
    a = a.zfill(n)
    b = b.zfill(n)

    m = n // 2
    a1, a0 = a[:m], a[m:]
    b1, b0 = b[:m], b[m:]

    p2 = karatsuba(a1, b1, base)
    p0 = karatsuba(a0, b0, base)
    p1 = karatsuba(school_add(a1, a0, base), school_add(b1, b0, base), base)

    mid = subtraction(p1, school_add(p2, p0, base), base)

    p2_shifted = p2 + "0" * (2 * (n - m))
    mid_shifted = mid + "0" * (n - m)

    res = school_add(school_add(p2_shifted, mid_shifted, base), p0, base)
    return res.lstrip("0") or "0"


def main():
    I1, I2, B = input().split()
    B = int(B)

    sum_result = school_add(I1, I2, B)
    prod_result = karatsuba(I1, I2, B)

    print(sum_result, prod_result, 0)


if __name__ == "__main__":
    main()
