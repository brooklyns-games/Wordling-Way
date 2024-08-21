import pygame

from button import *
from globs import *
from abstract import *


class Word(MySprite):
    words = OrderedGroup()  # needs a new init because ref is too broad
    def __init__(self, string, box):
        # ! passing box instead of self.box seems to solve everything-is-Button problem

        # print('before word')
        # print(self.__class__.__name__, self.groups())
        # test_instances(Button)
        # Word.instances
        super().__init__(string, box, Word.words)

    def update(self):
        # print('sdfdf', self.image)
        super().update()

class Parser:
    def __init__(self, *words):
        self.words = words

        print(self.words)


class Quest:
    def __init__(self, *words, name, desc):
        self.name = name
        self.desc = desc
        self.words = words

