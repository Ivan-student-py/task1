from collections import deque

def read_matrix(file_name):
    with open(file_name, 'r') as file:
        matrix = [list(map(int, line.split())) for line in file]
    return matrix

def find_shape(matrix, start_row, start_col, visited):
    rows, cols = len(matrix), len(matrix[0])
    queue = deque([(start_row, start_col)])
    shape_coords = []

    while queue:
        r, c = queue.popleft()
        if 0 <= r < rows and 0 <= c < cols and not visited[r][c] and matrix[r][c] == 1:
            visited[r][c] = True
            shape_coords.append((r, c))
            queue.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])

    return shape_coords

def is_square(shape_coords):
    min_row = min(r for r, c in shape_coords)
    max_row = max(r for r, c in shape_coords)
    min_col = min(c for r, c in shape_coords)
    max_col = max(c for r, c in shape_coords)

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r, c) not in shape_coords:
                return False
    return True

def count_shapes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    squares = 0
    circles = 0

    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 1 and not visited[r][c]:
                shape_coords = find_shape(matrix, r, c, visited)

                if is_square(shape_coords):
                    squares += 1
                else:
                    circles += 1

    return squares, circles

if __name__ == "__main__":
    matrix = read_matrix("00/task3/input.txt")
    squares, circles = count_shapes(matrix)
    print(squares, circles)