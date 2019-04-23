import turtle
from random import randrange
from freegames import square, vector
import time


class Game:
    def __init__(self, show=False):
        self.show = show

        self.food = vector(0, 0)
        self.snake = [vector(10, 0)]
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
        #turtle.ontimer(self.move, 100)

        return True

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

        #turtle.done()

        return len(self.snake)

    @staticmethod
    def inside(head):
        """Return True if head inside boundaries."""
        return -200 < head.x < 190 and -200 < head.y < 190
