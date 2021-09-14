from random import randrange
from collections import deque
import heapq


def number_of_char(two_dim_arr, character):
    counter = 0
    for row in two_dim_arr:
        for i in row:
            if i == character:
                counter += 1
    return counter


def char_to_str(s):
    new = ""
    for i in s:
        new += i
    return new


def print_maze(maze):
    for row in maze:
        print(char_to_str(row))


def get_neighbours(node):
    x, y = node
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def get_path(maze, visited, last):
    i = 0
    current_node = last
    while current_node != -1:
        y = current_node[0]
        x = current_node[1]
        if current_node == last:
            maze[x][y] = 'E'  # end
        elif visited[current_node] == -1:
            maze[x][y] = 'S'  # start
        else:
            maze[x][y] = 'p'  # path
        current_node = visited[current_node]
        i += 1
    return i - 1


def beautify(maze, closed, end):
    path_length = get_path(maze, closed, end)
    print_maze(maze)
    print("\n")
    print("S - start")
    print("E - end")
    print("O - opened node")
    print("C - closed node")
    print("p - path")
    print("X - wall")
    print("path length: ", path_length)
    nodes_expanded = number_of_char(maze, 'C') + number_of_char(maze, 'O') + 2 + path_length
    print("Nodes expanded: ", nodes_expanded)
    print("\n")


def get_maze_and_init_goal(file):
    f = open(file, 'r')
    lines = f.readlines()
    maze = []
    counter = 0
    for line in lines:
        if line[0] == 's' or line[0] == 'S':
            start = tuple(int(i) for i in line.replace('start ', '').split(','))
        elif line[0] == 'e' or line[0] == 'E':
            end = tuple(int(i) for i in line.replace('end', '').split(','))
        else:
            line = list(line)
            line = line[0: -1]  # removing \n
            maze.append(line)
    maze[start[1]][start[0]] = 'S'
    maze[end[1]][end[0]] = 'E'
    return maze, start, end


def random_search(maze, start, end):
    height = len(maze)
    width = len(maze[0])
    opened = []
    visited = {start: -1}
    opened.append(start)
    while opened:
        i = randrange(0, len(opened))
        current_node = opened[i]
        y, x = current_node
        opened.pop(i)

        if current_node != end:
            pass
        else:
            beautify(maze, visited, end)

        for n in get_neighbours(current_node):  # check all neighbours
            y, x = n
            if 0 < x < height and 0 < y < width and maze[x][y] != 'X' and n not in visited:
                opened.append(n)
                visited[n] = current_node
                if maze[x][y] not in ['S', 'E']:
                    maze[x][y] = 'O'  # mark as opened
        if maze[x][y] not in ['S', 'E']:
            maze[x][y] = 'C'  # mark as closed


def dfs(maze, start, end, no_animation=False):
    height = len(maze)
    width = len(maze[0])

    opened = []
    closed = {start: -1}
    opened.append(start)

    while opened:
        current_node = opened.pop()
        y, x = current_node

        if current_node == end:
            beautify(maze, closed, end)

        for n in get_neighbours(current_node):
            y_y, x_x = n
            if 0 < x_x < height and 0 < y_y < width and maze[x_x][y_y] != 'X' and n not in closed:
                opened.append(n)
                closed[n] = current_node

                if maze[x_x][y_y] not in ['S', 'E']:
                    maze[x_x][y_y] = 'O'  # opened

        if maze[x][y] not in ['S', 'E']:
            maze[x][y] = 'C'  # Closed


def bfs(maze, start, end):
    height = len(maze)
    width = len(maze[0])

    opened = deque()
    closed = {start: -1}
    opened.append(start)
    while opened:
        current_node = opened.popleft()
        y, x = current_node

        if current_node == end:
            beautify(maze, closed, end)

        for n in get_neighbours(current_node):
            y_y, x_x = n
            if 0 < x_x < height and 0 < y_y < width and n not in closed and maze[x_x][y_y] != 'X':
                opened.append(n)
                closed[n] = current_node

                if maze[x_x][y_y] not in ['S', 'E']:
                    maze[x_x][y_y] = 'O'  # opened node

        if maze[x][y] not in ['S', 'E']:
            maze[x][y] = 'C'  # closed node


def manhattan_distance(current_node, desired_node):
    current_node_x, current_node_y = current_node
    desired_node_x, desired_node_y = desired_node
    return abs(current_node_x - desired_node_x) + abs(current_node_y - desired_node_y)


def greedy(maze, start, end):
    height = len(maze)
    width = len(maze[0])

    opened = []
    heapq.heappush(opened, (0, start))  # initializing priority queue i.e. minheap
    previous = {start: -1}  # previous
    cost = {start: manhattan_distance(start, end)}

    while opened:
        current_node = opened[0]
        heapq.heappop(opened)
        y, x = current_node[1]

        if current_node[1] == end:
            beautify(maze, previous, end)

        for n in get_neighbours(current_node[1]):
            y_n = n[0]
            x_n = n[1]
            heuristic = manhattan_distance(n, end)

            if 0 < x_n < height and 0 < y_n < width and maze[x_n][y_n] != 'X' and n not in cost:
                cost[n] = heuristic
                heapq.heappush(opened, (heuristic, n))
                previous[n] = current_node[1]

                if maze[x_n][y_n] not in ['S', 'E']:
                    maze[x_n][y_n] = 'O'  # opened node

        if maze[x][y] not in ['S', 'E']:
            maze[x][y] = 'C'  # closed node


if __name__ == '__main__':
    maze, start, end = get_maze_and_init_goal('dataset/72.txt')
    random_search(maze, start, end)
    maze, start, end = get_maze_and_init_goal('dataset/72.txt')
    dfs(maze, start, end)
    maze, start, end = get_maze_and_init_goal('dataset/72.txt')
    bfs(maze, start, end)
    maze, start, end = get_maze_and_init_goal('dataset/72.txt')
    greedy(maze, start, end)
