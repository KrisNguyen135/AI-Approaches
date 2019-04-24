import turtle
from random import randrange
from freegames import square, vector
import time


class Game:
    def __init__(self, auto=None, show=False):
        self.auto = auto
        self.show = show

        self.food = vector(0, 0)
        self.snake = [vector(10, 0), vector(20, 0)]
        self.aim = vector(0, -10)

    def change(self, x, y):
        """Change snake direction."""
        self.aim.x = x
        self.aim.y = y

    def move(self):
        """Move snake forward one segment."""
        head = self.snake[-1].copy()
        head.move(self.aim)

        if not self.inside(head) or head in self.snake:
            if self.show:
                square(head.x, head.y, 9, 'red')
                turtle.update()
                time.sleep(1)

            return False

        self.snake.append(head)

        if head == self.food:
            self.food.x = randrange(-15, 15) * 10
            self.food.y = randrange(-15, 15) * 10
        else:
            self.snake.pop(0)

        turtle.clear()

        for body in self.snake:
            square(body.x, body.y, 9, 'black')

        square(self.food.x, self.food.y, 9, 'green')
        turtle.update()

        # Collect stats and feed to AI
        if self.auto is not None:
            delta_x = head.x - self.food.x
            delta_y = head.y - self.food.y
            direction = self.get_direction()
            move = self.auto(delta_x, delta_y, direction)
            if move == 0:
                self.change(0, 10)
            elif move == 1:
                self.change(-10, 0)
            elif move == 2:
                self.change(0, -10)
            elif move == 3:
                self.change(10, 0)

        return True

    def get_direction(self):
        # 0: up, 1: left, 2: down, 3: right
        head = self.snake[-1]
        neck = self.snake[-2]

        if head.x == neck.x:  # moving vertically
            if head.y > neck.y:
                return 0

            return 2

        if head.x < neck.x:
            return 3

        return 1

    def run(self):
        if self.show:
            turtle.setup(420, 420, 370, 0)
            turtle.hideturtle()
            turtle.tracer(False)
            turtle.listen()
            turtle.onkey(lambda: self.change(10, 0), 'Right')
            turtle.onkey(lambda: self.change(-10, 0), 'Left')
            turtle.onkey(lambda: self.change(0, 10), 'Up')
            turtle.onkey(lambda: self.change(0, -10), 'Down')

        keep_moving = self.move()
        while keep_moving:
            if self.show:
                time.sleep(0.1)

            keep_moving = self.move()

        return len(self.snake)

    @staticmethod
    def inside(head):
        """Return True if head inside boundaries."""
        return -200 < head.x < 190 and -200 < head.y < 190
