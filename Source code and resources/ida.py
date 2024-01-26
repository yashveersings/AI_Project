import time
import numpy as np

def print_maze(maze):
    for row in maze:
        print(row)

def find_position(maze, character):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == character:
                return x, y

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def ida_star(maze, start, end):
    def search(path, g, threshold):
        current = path[-1]
        f = g + manhattan_distance(current, end)

        if f > threshold:
            return f
        if current == end:
            return True

        min_cost = float('inf')
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current[0] + dx, current[1] + dy

            if next_y < 0 or next_y >= len(maze) or next_x < 0 or next_x >= len(maze[0]):
                continue
            if maze[next_y][next_x] != '#' and (next_x, next_y) not in path:
                path.append((next_x, next_y))
                t = search(path, g + 1, threshold)
                if t == True:
                    return True
                if t < min_cost:
                    min_cost = t
                path.pop()

        return min_cost

    threshold = manhattan_distance(start, end)
    path = [start]

    while True:
        t = search(path, 0, threshold)
        if t == True:
            return path, len(path) - 1
        if t == float('inf'):
            return None, None
        threshold = t

def generate_random_maze(width, height, p=0.9):
    maze = np.random.choice(['.', '#'], size=(height, width), p=[p, 1-p])
    maze[1, 1] = 'P'
    maze[-2, -2] = 'G'
    return [''.join(row) for row in maze]

def main(iterations=10):
    total_time = 0
    total_cost = 0
    success_count = 0

    for i in range(iterations):
        random_maze = generate_random_maze(20, 10)

        start = find_position(random_maze, 'P')
        end = find_position(random_maze, 'G')

        start_time = time.time()
        result = ida_star(random_maze, start, end)
        end_time = time.time()

        print(f"Iteration {i+1}:")
        print_maze(random_maze)
        if result[0] is not None:
            path, cost = result
            total_time += end_time - start_time
            total_cost += cost
            success_count += 1
            print(f"Path found with cost {cost}")
        else:
            print("No path found")
        print()

    if success_count > 0:
        print("Average Time: {:.4f} seconds".format(total_time / success_count))
        print("Average Score: {:.2f}".format(total_cost / success_count))
    else:
        print("No path found for all iterations.")

if __name__ == "__main__":
    main()
