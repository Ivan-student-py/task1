N = int(input())
unique_numbers = []
for _ in range(N):
    number = int(input())
    if number not in unique_numbers:
        unique_numbers.append(number)
print(len(unique_numbers))