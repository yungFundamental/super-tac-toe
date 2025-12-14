from enum import Enum


class XO(Enum):
    blank = 0
    x = 10
    o = -10


class Cell:
    length = 68
    height = 57

    def __init__(self, start_x, start_y, x_img, o_img):
        self.start_x = start_x
        self.start_y = start_y
        self.id = XO.blank
        self.x_img = x_img
        self.o_img = o_img

    def draw(self, screen):
        if self.id == XO.x:
            screen.blit(self.x_img, (self.start_x, self.start_y))
        if self.id == XO.o:
            screen.blit(self.o_img, (self.start_x, self.start_y))


def reverse(xo):
    if xo == XO.x:
        return XO.o
    if xo == XO.o:
        return XO.x
    return XO.blank


