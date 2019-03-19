import random
import turtle
from freegames import vector

import time
import tkinter
from math import sqrt


class Game:
    def __init__(self, net=None, show=False):
        self.net = net
        self.show = show

        self.bird = vector(0, 0)
        self.balls = []
        self.score = 0
        #self.root = tkinter.Tk()

    def tap(self, x, y):
        """Move bird up in response to screen tap."""
        up = vector(0, 30)
        self.bird.move(up)

    def draw(self, alive):
        """Draw screen objects."""
        turtle.clear()

        turtle.goto(self.bird.x, self.bird.y)

        if alive:
            turtle.dot(10, 'green')
        else:
            turtle.dot(10, 'red')

        for ball in self.balls:
            turtle.goto(ball.x, ball.y)
            turtle.dot(20, 'black')

        turtle.update()

    def move(self):
        """Update object positions."""
        self.score += 1
        self.bird.y -= 5

        for ball in self.balls:
            ball.x -= 3

        if random.randrange(10) == 0:
            y = random.randrange(-199, 199)
            ball = vector(199, y)
            self.balls.append(ball)

        while len(self.balls) > 0 and not Game.inside(self.balls[0]):
            self.balls.pop(0)

        if not Game.inside(self.bird):
            if self.show:
                self.draw(False)
                time.sleep(1)
            #self.root.destroy()
            #self.root.quit()
            return False

        for ball in self.balls:
            if abs(ball - self.bird) < 15:
                if self.show:
                    self.draw(False)
                    time.sleep(1)
                #self.root.destroy()
                #self.root.quit()
                return False

        if self.show:
            self.draw(True)

        # Collect stats and feed to neural net
        if self.net is not None:
            inputs = self.get_net_stats()
            outputs = self.net.activate(inputs)
            result = outputs.index(max(outputs))
            if result == 0:
                self.tap(None, None)

        #turtle.ontimer(self.move, 50)

        return True

    def get_net_stats(self, num_balls=5):
        """Return inputs for the neural networks."""
        distances = []

        for ball in self.balls:
            distances.append(sqrt(
                (ball.x-self.bird.x)**2 + (ball.y-self.bird.y)**2))

        sorted_balls = [
            ball for _, ball in sorted(zip(distances, self.balls),
                                       key=lambda pair: pair[0])
        ][: num_balls]

        stats = [self.bird.x] + [ball.x for ball in sorted_balls] \
               + [self.bird.y] + [ball.y for ball in sorted_balls]

        num_paddings = 2 + num_balls * 2 - len(stats)
        if num_paddings > 0:
            stats += [400] * num_paddings

        return stats

    def run(self):
        if self.show:
            turtle.setup(420, 420, 0, 0)
            turtle.hideturtle()
            turtle.up()
            turtle.tracer(False)
            turtle.onscreenclick(self.tap)

        keep_moving = self.move()
        while keep_moving:
            if self.show:
                time.sleep(0.05)

            keep_moving = self.move()
        #turtle.done()

        return self.score

    @staticmethod
    def inside(point):
        """Return True if point on screen."""
        return -200 < point.x < 200 and -200 < point.y < 200
