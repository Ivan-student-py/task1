def generate_pascals_triangle(n):
    triangle = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1,i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle

def main():
    try:
        n=int(input("Введите количество строк: "))
        if n <= 0:
            print("Natural number was expected")
            return
        pascals_triangle = generate_pascals_triangle(n)
        for row in pascals_triangle:
            print(" ".join(map(str, row)))
    except ValueError:
        print("Natural number was expected")

if __name__ == "__main__":
    main()