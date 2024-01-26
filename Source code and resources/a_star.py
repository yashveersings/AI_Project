import time
import heapq
import numpy as np


def print_maze(maze):
    for row in maze:
        print(row)


def find_position(maze, character):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == character:
                return x, y


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(maze, start, end):
    heap = [(0, [start])]
    visited = set()

    while heap:
        (cost, path) = heapq.heappop(heap)
        (x, y) = path[-1]

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (x, y) == end:
            return path, cost

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = x + dx, y + dy

            if next_y < 0 or next_y >= len(maze) or next_x < 0 or next_x >= len(maze[0]):
                continue

            if maze[next_y][next_x] != '#' and (next_x, next_y) not in visited:
                next_cost = cost + 1  # Assume all steps cost 1
                priority = next_cost + manhattan_distance(next_x, next_y, end[0], end[1])
                heapq.heappush(heap, (priority, path + [(next_x, next_y)]))

    return (None, None)


def generate_random_maze(width, height, p=0.7):
    maze = np.random.choice(['.', '#'], size=(height, width), p=[p, 1-p])
    maze[1, 1] = 'P'
    maze[-2, -2] = 'G'
    return [''.join(row) for row in maze]


def main(iterations=1000):
    total_time = 0
    total_cost = 0
    success_count = 0

    for i in range(iterations):
        random_maze = generate_random_maze(20, 10)

        start = find_position(random_maze, 'P')
        end = find_position(random_maze, 'G')

        start_time = time.time()
        result = a_star(random_maze, start, end)
        end_time = time.time()

        if result[0] is not None:
            path, cost = result
            total_time += end_time - start_time
            total_cost += cost
            success_count += 1

    if success_count > 0:
        print("Average Time: {:.4f} seconds".format(total_time / success_count))
        print("Average Score: {:.2f}".format(total_cost / success_count))
    else:
        print("No path found for all iterations.")


if __name__ == "__main__":
    main()
