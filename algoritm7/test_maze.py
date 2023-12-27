"""Тесты для модуля maze"""
import unittest
from maze import get_direction_offset, get_opposite_direction, MazeGenerator, jump_point_search, \
    path_first_last, check_add_walls


class TestMazeGenerator(unittest.TestCase):
    def test_get_direction_offset(self):
        self.assertEqual(get_direction_offset(1), (0, -1))
        self.assertEqual(get_direction_offset(2), (0, 1))
        self.assertEqual(get_direction_offset(4), (1, 0))
        self.assertEqual(get_direction_offset(8), (-1, 0))

    def test_get_opposite_direction(self):
        self.assertEqual(get_opposite_direction(1), 2)
        self.assertEqual(get_opposite_direction(2), 1)
        self.assertEqual(get_opposite_direction(4), 8)
        self.assertEqual(get_opposite_direction(8), 4)

    def test_is_within_bounds(self):
        maze = MazeGenerator(5, 5)
        self.assertTrue(maze.is_within_bounds(3, 3))
        self.assertTrue(maze.is_within_bounds(0, 0))
        self.assertFalse(maze.is_within_bounds(5, 5))
        self.assertFalse(maze.is_within_bounds(-1, 2))


class TestMazeSolver(unittest.TestCase):
    def test_jump_point_search(self):
        maze = [
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

        start = (0, 0)
        end = (4, 4)
        path, distance = jump_point_search(maze, start, end)
        self.assertEqual(path, [(0, 0), (1, 1), (2, 2), (2, 3), (3, 4), (4, 4)])
        self.assertEqual(distance, 6.24)

    def test_path_first_last(self):
        maze = [
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

        path, distance = path_first_last(maze)
        self.assertEqual(path, [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (4, 3), (4, 4)])
        self.assertEqual(distance, 6.83)


class TestCheckAddWalls(unittest.TestCase):
    def test_small_maze(self):
        # Проверка для маленького лабиринта
        self.assertEqual(check_add_walls(2, 2), 1)
        self.assertEqual(check_add_walls(3, 3), 1)

    def test_medium_maze(self):
        # Проверка для среднего лабиринта
        self.assertEqual(check_add_walls(4, 4), 2)
        self.assertEqual(check_add_walls(6, 6), 2)

    def test_large_maze(self):
        # Проверка для большого лабиринта
        self.assertEqual(check_add_walls(10, 10), 4)
        self.assertEqual(check_add_walls(15, 15), 8)

    def test_recursive(self):
        # Проверка для рекурсивного расширения лабиринта
        self.assertEqual(check_add_walls(14, 14), 6)
        self.assertEqual(check_add_walls(18, 18), 8)
        self.assertEqual(check_add_walls(22, 22), 10)
        self.assertEqual(check_add_walls(23, 23), 12)


class TestBinGenerator(unittest.TestCase):
    def test_convert_maze_to_binary_square(self):
        maze = MazeGenerator(4, 4)
        maze.generate()
        maze.grid = [[2, 6, 12, 10], [3, 3, 6, 9], [5, 9, 5, 10], [4, 12, 12, 9]]
        test_maze = [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        bin_maze = maze.convert_maze_to_binary()
        self.assertEqual(bin_maze, test_maze)


if __name__ == '__main__':
    unittest.main()
