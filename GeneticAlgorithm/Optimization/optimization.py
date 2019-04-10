import random


class Game:
    def __init__(self, degree, x_limits, coefs):
        self.degree = degree
        self.x_limits = x_limits
        self.coefs = coefs

    def get_value(self, x):
        if self.x_limits[0] <= x <= self.x_limits[1]:
            return sum([x**i * self.coefs[i] for i in range(self.degree + 1)])

        return False
