import pygame

from button import *
from globs import *



class Word(Button):
    def __init__(self, string, word_box, input_box):
        self.box = word_box
        # self.string = string
        super().__init__(string, self.box)  # this adds to self.box.items
        self.add(self.box.words,)

        # print(self.string, string)
        # For initialization
        self.index = 0
        self.word_box = word_box
        self.input_box = input_box
        self.available_boxes = (self.word_box, input_box)  # idk if this can be used


    def default_xy(self):
        self.update_index()
        box = self.box.rect
        x, y = box.x, (box.y + (self.index - 0) * 60)
        return x, y

    def toggle_box(self):
        """switches between default box and input box. adds 1 self """
        # print('toggling')
        other = None
        if self.box == self.word_box:
            other = self.input_box
        elif self.box == self.input_box:
            other = self.word_box
        else:
            raise ValueError

        self.box.words.remove(self)
        other.words.add(self)  # chill

        self.box = other  # the switch
        self.update_index()  # update all boxes .words?

        return self.box

    def set_click(self, switch):
        super().set_click(switch)
        if not switch:
            self.state = False

    def click(self):

        if not self.state:
            # print('toggle', self.clicked, self.state)
            self.toggle_box()
            self.state = True

    def update_index(self):
        self.index = self.box.get_index(self)

    def update_rect(self):
        pass

    def draw_me(self):
        self.image = self.font.render(self.name, True, self.color)
        pygame.draw.rect(self.image, self.color, ([0, 0], self.image.get_size()), 5, border_radius=15)

    def update(self):
        super().update()


        # self.rect.update([self.x, self.y], self.image.get_size())


class Parser:
    def __init__(self, *words):
        self.words = words


class Quest:
    def __init__(self, *words, name, desc):
        self.name = name
        self.desc = desc
        self.words = words

