from __future__ import annotations

import os
import random
import sys
import pygame
import heapq
import math


def get_direction_offset(direction: int) -> tuple:
    """
    This function takes a direction code and returns an offset for it
    :param direction: Direction of maze generation
    :return: Offset for the direction code
    """
    offsets = {1: (0, -1), 2: (0, 1), 4: (1, 0), 8: (-1, 0)}
    return offsets[direction]


def get_opposite_direction(direction):
    """
    Accepts the direction code and returns the opposite direction
    :param direction: Code of the direction of generation
    :return: The opposite direction of generation
    """
    opposites = {1: 2, 2: 1, 4: 8, 8: 4}
    return opposites[direction]


class MazeGenerator:
    """
    A class that is initialized with the specified dimensions and an optional seed for generating random numbers
    """
    def __init__(self, width: int, height: int, seed=None):
        """
        Initializing the maze
        :param width: Width of the maze
        :param height: Height of the maze
        :param seed: Depth for generating random numbers.
        """
        if width * height < 4:
            raise ValueError("The maze should be at least 2 by 2")
        self.width = width
        self.height = height
        self.seed = seed if seed else random.randint(0, 0xFFFFFFFF)
        self.grid = [[0] * self.width for _ in range(self.height)]

    def generate(self):
        """
        Random number generation.
        """
        random.seed(self.seed)
        self.carve_passages_from(0, 0)

    def carve_passages_from(self, x: int, y: int):
        """
        Starts cutting passages in the maze, starting from (0, 0)
        Selects a random direction and moves, creating passages
        :param x: Coordinate of x in maze
        :param y: Coordinate of y in maze
        """
        directions = [1, 2, 4, 8]
        random.shuffle(directions)

        for direction in directions:
            dx, dy = get_direction_offset(direction)
            nx, ny = x + dx, y + dy

            if self.is_within_bounds(nx, ny) and self.grid[ny][nx] == 0:
                self.grid[y][x] |= direction
                self.grid[ny][nx] |= get_opposite_direction(direction)
                self.carve_passages_from(nx, ny)

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        Checks whether the coordinates (x, y) are within the boundaries of the maze
        :param x: Coordinate of x in maze
        :param y: Coordinate of y in maze
        :return: Finding coordinates inside the maze
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def print_maze(self):
        """
        Outputs the maze to the console, and also saves it to a text file
        """
        maze_array = [(" " + "_" * (self.width * 2 - 1))]
        print(" " + "_" * (self.width * 2 - 1))
        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                row += " " if self.grid[y][x] & 2 != 0 else "_"
                if x + 1 < self.width and self.grid[y][x] & 4 != 0:
                    row += " " if (self.grid[y][x] | self.grid[y][x + 1]) & 2 != 0 else "_"
                else:
                    row += "|"
            print(row)
            maze_array.append(row)

        if os.path.exists("maze.txt"):
            os.remove("maze.txt")

        with open("maze.txt", "a") as file:
            for line in maze_array:
                file.write(line + "\n")

    def print_parameters(self):
        """
        Outputs the parameters of the generated maze
        """
        print(f"{sys.argv[0]} {self.width} {self.height} {self.seed}")

    def draw_maze(self):
        """
        Draws a maze using the pygame module in a separate window
        :return: Window with the pygame module
        """
        pygame.init()
        cell_size = 50
        wall_thickness = 1
        screen_width = self.width * cell_size
        screen_height = self.height * cell_size
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))  # White background
            for y in range(self.height):
                for x in range(self.width):
                    cx = x * cell_size
                    cy = y * cell_size

                    if self.grid[y][x] & 1 == 0:
                        pygame.draw.rect(screen, (0, 0, 0), (cx, cy, cell_size, wall_thickness))  # Top wall
                    if self.grid[y][x] & 2 == 0:
                        pygame.draw.rect(screen, (0, 0, 0), (cx, cy + cell_size - wall_thickness, cell_size,
                                                             wall_thickness))  # Bottom wall
                    if self.grid[y][x] & 4 == 0:
                        pygame.draw.rect(screen, (0, 0, 0), (cx + cell_size - wall_thickness, cy, wall_thickness,
                                                             cell_size))  # Right wall
                    if self.grid[y][x] & 8 == 0:
                        pygame.draw.rect(screen, (0, 0, 0), (cx, cy, wall_thickness, cell_size))  # Left wall

            pygame.display.flip()
            clock.tick(60)  # Limit FPS to 60

    def save_maze_image(self, filename: str):
        """
        Saves the maze to the file specified by the user
        :param filename: The path to file
        :return: The image of maze in filename
        """
        cell_size = 50
        wall_thickness = 1  # Увеличение толщины стенок
        image_width = self.width * cell_size
        image_height = self.height * cell_size
        image = pygame.Surface((image_width, image_height))
        image.fill((255, 255, 255))  # White background

        for y in range(self.height):
            for x in range(self.width):
                cx = x * cell_size
                cy = y * cell_size

                if self.grid[y][x] & 1 == 0:
                    pygame.draw.rect(image, (0, 0, 0), (cx, cy, cell_size, wall_thickness))  # Top wall
                if self.grid[y][x] & 2 == 0:
                    pygame.draw.rect(image, (0, 0, 0), (cx, cy + cell_size - wall_thickness, cell_size,
                                                        wall_thickness))  # Bottom wall
                if self.grid[y][x] & 4 == 0:
                    pygame.draw.rect(image, (0, 0, 0), (cx + cell_size - wall_thickness, cy, wall_thickness,
                                                        cell_size))  # Right wall
                if self.grid[y][x] & 8 == 0:
                    pygame.draw.rect(image, (0, 0, 0), (cx, cy, wall_thickness, cell_size))  # Left wall

        pygame.image.save(image, filename)

    def convert_maze_to_binary(self) -> list[list[int]]:
        """
        Converts the maze from writing numbers [1, 2, 4, 8] to bitwise
        :return: Array in a bit of notation (0 and 1)
        """
        max_upper_walls = 0
        max_side_walls = 0
        for column in range(self.height):
            count_upper = 0
            flag = 0
            for element in range(self.width):
                if element & 2 == 0:
                    count_upper += 1
                if element & 4 == 0:
                    flag = 1
            if count_upper > max_upper_walls:
                max_upper_walls = count_upper
            if flag == 1:
                max_side_walls += 1

        binary_maze = None
        count_add = check_add_walls(self.width, self.height)
        if self.width == self.height:
            binary_maze = [[0] * (max_side_walls + self.width) for _ in
                           range(self.height + max_upper_walls + count_add)]
        if self.height > self.width:
            binary_maze = [[0] * (max_side_walls + self.width) for _ in
                           range(self.height + max_upper_walls + count_add * (self.height - self.width + 1))]
        if self.width > self.height:
            binary_maze = [[0] * (max_side_walls + self.width + count_add * (self.width - self.height + 2)) for _ in
                           range(self.height + max_upper_walls + count_add)]
        count_row = 0
        for row in self.grid:
            count_element = 0
            for element in row:
                if element & 4 == 0:  # Right wall
                    binary_maze[(count_row * 2)][(1 + (count_element * 2))] = 1
                if element & 2 == 0:  # Bottom wall
                    binary_maze[1 + (count_row * 2)][(count_element * 2)] = 1
                if count_row > 0:
                    if element & 4 == 0 and element & 1 == 0:  # Проверка верхнего правого угла
                        binary_maze[(count_row * 2) - 1][(count_element * 2) + 1] = 1
                if count_element > 0:
                    if element & 2 == 0 and row[count_element - 1] & 2 == 0:
                        binary_maze[1 + (count_row * 2)][(count_element * 2) - 1] = 1
                    if element & 8 == 0 and element & 2 == 0:  # Проверка нижнего левого угла
                        binary_maze[(count_row * 2) + 1][(count_element * 2) - 1] = 1
                    if element & 4 == 0 and element & 2 == 0:  # Проверка нижнего правого угла
                        binary_maze[(count_row * 2) + 1][(count_element * 2) + 1] = 1
                if count_element > 0 and count_row > 0:
                    if element & 8 == 0 and self.grid[count_row - 1][count_element] & 8 == 0:  # Стенки левые
                        binary_maze[(count_row * 2) - 1][(count_element * 2) - 1] = 1
                    if element & 4 == 0 and self.grid[count_row - 1][count_element] & 4 == 0:  # Стенки правые
                        binary_maze[(count_row * 2) - 1][(count_element * 2) + 1] = 1
                    if element & 8 == 0 and element & 1 == 0:  # Проверка верхнего левого угла
                        binary_maze[(count_row * 2) - 1][(count_element * 2) - 1] = 1
                count_element += 1
            count_row += 1

        binary_maze = binary_maze[:self.height * 2 - 1]
        for i in range(len(binary_maze)):
            binary_maze[i] = binary_maze[i][:self.width * 2 - 1]
            print(binary_maze[i])
        return binary_maze


def check_add_walls(wide: int, top: int, add_count: int = 4) -> int:
    """
    This function calculates the number of additional dimensions of the maze
    :param wide: The width of maze
    :param top: The height of maze
    :param add_count: Standard addition of maze sizes
    :return: Additional expansion of the maze
    """
    if wide <= 2 or top <= 2:
        return 1
    if wide <= 3 or top <= 3:
        return 1
    if wide <= 4 or top <= 4:
        return 2
    if wide <= 6 or top <= 6:
        return 2
    if wide <= 10 or top <= 10:
        return add_count
    if wide > 9 or top > 9:
        return check_add_walls((wide - 4), (top - 4), (add_count + 2))


def jump_point_search(grid: list[list[int]], start: tuple, end: tuple) -> (int, float):
    """
    This function performs the "Sidewinder" algorithm, which generates a maze for users
    :param grid: A maze in binary notation (of ones and zeros)
    :param start: The starting point in finding the path
    :param end: The ending point in finding the path
    :return: The found path, as well as the distance in the traveled path, otherwise None
    """
    for row in grid:
        row.append(1)
    grid.append([1] * len(grid[0]))

    def neighbors(node: tuple):
        """
        Defines neighbors for a given point in the grid
        :param node: Coordinates of the point
        """
        x, y = node
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                if 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]):
                    yield x + dx, y + dy

    def euclidean_distance(node1: tuple, node2: tuple) -> float:
        """
        Calculates the Euclidean distance between two points
        :param node1: Coordinates of the point 1
        :param node2: Coordinates of the point 2
        :return: Euclidean_distance
        """
        x1, y1 = node1
        x2, y2 = node2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def jump(node: tuple, parent: tuple) -> tuple or None:
        """
        Recursively searches for "jumps" from the current point to the next point on the way to the target point
        :param node: Coordinates of the point 1
        :param parent: Coordinates of the point 2
        :return: Coordinates of the point jump or None
        """
        x, y = node
        px, py = parent
        dx, dy = x - px, y - py

        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])) or grid[x][y] == 1:
            return None

        if node == end:
            return node

        if dx != 0 and dy != 0:
            if grid[x - dx][y] == 1 or grid[x][y - dy] == 1:
                return node

            if jump((x + dx, y), node) or jump((x, y + dy), node):
                return node

        if dx != 0:
            if (y + 1) <= len(grid):
                if grid[x][y + 1] == 1 or grid[x][y - 1] == 1:
                    return node

        if dy != 0:
            if (x + 1) < len(grid):
                if grid[x + 1][y] == 1 or grid[x - 1][y] == 1:
                    return node

        return jump((x + dx, y + dy), node)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            path.insert(0, start)
            return path, round(g_score[end], 2)

        for neighbor in neighbors(current):
            jump_node = jump(neighbor, current)
            if jump_node:
                tentative_g_score = g_score[current] + euclidean_distance(current, jump_node)
                if tentative_g_score < g_score.get(jump_node, float("inf")):
                    came_from[jump_node] = current
                    g_score[jump_node] = tentative_g_score
                    f_score = tentative_g_score + euclidean_distance(jump_node, end)
                    heapq.heappush(open_set, (f_score, jump_node))

    return None, float("inf")


def path_first_last(maze: list[list[int]]) -> (int, int):
    """
    Finding the path from the first free point to the last free point in the maze
    :param maze: A maze in binary notation (of ones and zeros)
    :return: The found path, as well as the distance in the traveled path
    """
    start = ()
    finish = ()
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 0:
                if not start:
                    start = (j, i)
                finish = (i, j)
    print(f"Start point: ", start, "\nEnd point: ", finish)
    path, distance = jump_point_search(maze, start, finish)
    return path, distance
