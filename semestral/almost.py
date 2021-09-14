import pygame
import random

game_width = 10
game_height = 20

#        R    G    B
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHTBLUE = (102, 178, 255)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)
BACK_COLOR = (233, 233, 233)
WHITE = (255, 255, 255, 1)

colors = [
    (0, 0, 0),
    (155, 155, 0),
    (0, 155, 0),
    (80, 34, 22),
    (155, 0, 0),
    (0, 0, 155),
    (255, 128, 0),
]
counter = 0


# this class is required for buttons control
class Event:
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


# here i use the simpliest idea possible in selecting the best holes
class TetrisBot:

    def __init__(self, game_field, game_figure):
        self.game_field = game_field
        self.game_figure = game_figure

    # we re configuring the position and the rotation in accordance with the best results got from the simulation
    def run_algo(self):
        global counter
        counter += 1
        if counter < 3:
            return []
        counter = 0
        rotation, position = self.best_rotation_position(self.game_field, self.game_figure)
        if self.game_figure.rotation != rotation:
            e = Event(pygame.KEYDOWN, pygame.K_UP)
        elif self.game_figure.x < position:
            e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
        elif self.game_figure.x > position:
            e = Event(pygame.KEYDOWN, pygame.K_LEFT)
        else:
            e = Event(pygame.KEYDOWN, pygame.K_SPACE)
        return [e]

    @staticmethod
    def bumps(game_field, x, y, game_figure_image):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game_figure_image:
                    if i + y > game_height - 1 or \
                            j + x > game_width - 1 or \
                            j + x < 0 or \
                            game_field[i + y][j + x] > 0:
                        intersection = True
        return intersection

    def simulate(self, game_field, x, y, game_figure_image):
        while not self.bumps(game_field, x, y, game_figure_image):
            y += 1
        y -= 1

        height = game_height
        holes = 0
        filled = []
        breaks = 0
        for i in range(game_height - 1, -1, -1):
            it_is_full = True
            prev_holes = holes
            for j in range(game_width):
                u = '_'
                if game_field[i][j] != 0:
                    u = "x"
                for ii in range(4):
                    for jj in range(4):
                        if ii * 4 + jj in game_figure_image:
                            if jj + x == j and ii + y == i:
                                u = "x"

                if u == "x" and i < height:
                    height = i
                if u == "x":
                    filled.append((i, j))
                    for k in range(i, game_height):
                        if (k, j) not in filled:
                            holes += 1
                            filled.append((k, j))
                else:
                    it_is_full = False
            if it_is_full:
                breaks += 1
                holes = prev_holes

        return holes, game_height - height - breaks

    def best_rotation_position(self, game_field, game_figure):

        best_height = game_height
        best_holes = game_height * game_width

        best_position = None
        best_rotation = None

        for rotation in range(len(game_figure.figures[game_figure.type])):
            fig = game_figure.figures[game_figure.type][rotation]
            for j in range(-3, game_width):
                if not self.bumps(
                        game_field,
                        j,
                        0,
                        fig):
                    holes, height = self.simulate(
                        game_field,
                        j,
                        0,
                        fig
                    )
                    if best_position is None or best_holes > holes or \
                            best_holes == holes and best_height > height:
                        best_height = height
                        best_holes = holes
                        best_position = j
                        best_rotation = rotation
        return best_rotation, best_position


# this is the class in charge for the next falling figure
class FigureImage:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self):
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def set_up(self, type, color):
        self.type = type
        self.color = color
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation - 1) % len(self.figures[self.type])


# this is the class of the field
class Tetris:
    level = 2
    game_level = 1
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    next_figure = None
    next_figure_image = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        if self.next_figure == None:
            self.figure = Figure(3, 0)
            self.next_figure_image = FigureImage()
            self.next_figure = Figure(3, 0)

            self.next_figure.color = self.next_figure_image.color
            self.next_figure.type = self.next_figure_image.type
            self.next_figure.rotation = self.next_figure_image.rotation
        else:
            self.figure = Figure(3, 0)
            self.figure.color = self.next_figure.color
            self.figure.y = self.next_figure.y
            self.figure.x = self.next_figure.x
            self.figure.type = self.next_figure.type
            self.figure.rotation = self.next_figure.rotation

            self.next_figure_image = FigureImage()

            self.next_figure.color = self.next_figure_image.color
            self.next_figure.type = self.next_figure_image.type
            self.next_figure.rotation = self.next_figure_image.rotation

    def next_figure_create(self):
        self.next_figure = Figure(3, 0)

    def bumps(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += (self.game_level * (lines ** 2))
        self.game_level = (self.score // 10) + 1

    def go_space(self):
        while not self.bumps():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.bumps():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.bumps():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.bumps():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.bumps():
            self.figure.rotation = old_rotation


def run_game():
    # Initialize the game engine
    pygame.init()

    # Setting the dize and screen for our field
    size = (500, 600)
    screen = pygame.display.set_mode(size)

    # Setting the name
    pygame.display.set_caption("Tetris bot")

    # Loop until the user finishes
    done = False
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20, 10)
    counter_game = 0

    pressing_down = False

    while not done:
        if game.figure is None:
            game.next_figure_create()
            game.new_figure()

        counter_game += 1
        if counter_game > 100000:
            counter_game = 0
        
        if counter_game % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()
        # for event in list(pygame.event.get()) + TetrisBot.run_a;go(TetrisBot(game.field, game.figure)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

        screen.fill(BACK_COLOR)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                                 3)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 1])

        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, GRAY,
                                 [game.x + game.zoom * j + 250, game.y + game.zoom * i + 70, game.zoom, game.zoom], 2)

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        if game.next_figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, colors[game.next_figure.color],
                                         [game.x + game.zoom * (j + game.next_figure.x) + 190,
                                          game.y + game.zoom * (i + game.next_figure.y) + 70,
                                          game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text2 = font.render("Level: " + str(game.game_level), True, BLACK)
        text3 = font.render("FPS:" + str(clock.tick(fps)), True, BLACK)
        text4 = font.render("Next figure:", True, BLACK)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [340, 20])
        screen.blit(text2, [340, 70])
        screen.blit(text3, [0, 0])
        screen.blit(text4, [340, 100])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


def run_game_ai():
    # Initialize the game engine
    pygame.init()

    # Setting the dize and screen for our field
    size = (500, 600)
    screen = pygame.display.set_mode(size)

    # Setting the name
    pygame.display.set_caption("Tetris bot")

    # Loop until the user finishes
    done = False
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20, 10)
    counter_game = 0

    pressing_down = False

    while not done:
        if game.figure is None:
            game.next_figure_create()
            game.new_figure()

        counter_game += 1
        if counter_game > 100000:
            counter_game = 0

        if counter_game % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()
        for event in list(pygame.event.get()) + TetrisBot.run_algo(TetrisBot(game.field, game.figure)):
            # for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

        screen.fill(BACK_COLOR)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                                 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 1])

        for i in range(4):
            for j in range(4):
                pygame.draw.rect(screen, GRAY,
                                 [game.x + game.zoom * j + 250, game.y + game.zoom * i + 70, game.zoom, game.zoom], 2)

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        if game.next_figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, colors[game.next_figure.color],
                                         [game.x + game.zoom * (j + game.next_figure.x) + 190,
                                          game.y + game.zoom * (i + game.next_figure.y) + 70,
                                          game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text2 = font.render("Level: " + str(game.game_level), True, BLACK)
        text3 = font.render("FPS:" + str(clock.tick(fps)), True, BLACK)
        text4 = font.render("Next figure:", True, BLACK)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [340, 20])
        screen.blit(text2, [340, 70])
        screen.blit(text3, [0, 0])
        screen.blit(text4, [340, 100])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


def main():
    print("Press 1 if you want to play or anything else to see Algorithm playing Tetris.")
    string = str(input())

    # output
    print(string)
    if string == '1':
        run_game()
    else:
        run_game_ai()
    return 0


if __name__ == "__main__":
    main()
