n = int(input())

if n < 0:
    print(False)
else:
    original = n
    reversed_number = 0
    while n > 0:
        last_digit = n % 10
        reversed_number = reversed_number * 10 + last_digit
        n //= 10
    print(original == reversed_number)