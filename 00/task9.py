N, x0 = map(float, input().split())
N = int(N)
coefficients = [float(input()) for _ in range(N + 1)]
coefficients.reverse()
derivative_value = 0.0
for i in range(1, N + 1):
    derivative_value += i * coefficients[i] * (x0 ** (i-1))
print(f"{derivative_value:.3f}")