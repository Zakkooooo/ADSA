def school_add(I1: str, I2: str, B: int) -> str:
    # Make both numbers the same length by adding zeros
    n = max(len(I1), len(I2))
    I1 = I1.zfill(n)
    I2 = I2.zfill(n)

    carry = 0 # Carry from previous column
    result = [] # To store the result digits

    # Process digits from left to right
    for i in range(n - 1, -1, -1):
        d1 = int(I1[i]) # Digit from I1
        d2 = int(I2[i]) # Digit from I2
        total = d1 + d2 + carry

        result.append(str(total % B))  # Current digit in base B 
        carry = total // B  # Update carry

    # Add final carry if it exists
    if carry > 0:
        result.append(str(carry))

    # Reverse result to get correct order
    result.reverse()
    return ''.join(result)


def main():
    # Read input
    I1_str, I2_str, B_str = input().split()
    B = int(B_str)

    # Perform addition
    sum_result = school_add(I1_str, I2_str, B)

    # Print only the sum result
    print(sum_result)