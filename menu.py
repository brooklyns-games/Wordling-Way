import pygame
from globs import *
from words import *
from abstract import OrderedGroup, Thing

import usefuls

# pygame.font.init()


class Interface(Thing):
    instances = pygame.sprite.Group()
    def __init__(self, rect=(0, 0, W, H), name=None, color='light blue'):
        super().__init__(name, rect, Interface.instances)
        # print('interface', name, len(self.groups()))
        # self.name = name  # for developer reference
        # self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)
        self.color = color

        self.mini_rect = self.rect.copy()

        self.items = OrderedGroup()  # other things that are not Word()s


    def draw_me(self):
        # self.mini_rect = self.rect.inflate(-50, -50)  # padding
        # self.mini_rect = pygame.draw.rect(self.image, self.color,
        #                                   [(25, 25), self.rect.size])
        self.image.fill(self.color)
        return self.image

    # def update(self):
    #     self.draw_me()

    def get_rect(self, box):
        # I forgot what this does. Related to param bind?
        try:

            # print(box.name, self.items.get_order(box))
            return pygame.Rect(self.rect.x + self.items.get_order(box) * (self.rect.width / len(self.items)),
                               self.rect.y, int(self.rect.width / len(self.items)), self.rect.height)
        except ValueError:
            raise ValueError


class Box(Interface):

    def __init__(self, rect=(0, 0, W, H), name=None, color='orange', sticky=True, bind=None, weight=1):
        """
        :param sticky: Removing a word does not affect positions
        :param bind: Interface(), overrides self.rect
        """
        self.words = OrderedGroup(name)  # made of Word()s
        self.bind = bind

        super().__init__(rect, name, color)
        self.write_format = False
        self.sticky = sticky  # for non-text boxes

        self.rows = [[]]
        self.positions = {}

        self.update()


    def update(self):

        super().update()

        if type(self.bind) is Interface:
            self.add(self.bind.items)  # must be phrased to activate OrderedGroup.add_internal()
            self.rect = self.bind.get_rect(self)

    def get_index(self, sprite):
        """Returns where the sprite is inside the group. Sticky list sprites always have the same place.
        This runs outside of self.update(), called by a self.words item"""
        self.update()  # words_list and words must sync!
        if not self.write_format:  # list format
            if len(self.words) > 0:
                if not self.sticky:
                    return 0, self.words.list_names().index(sprite.name) * sprite.rect.height
                else:
                    # print(self.words.name, sprite.string, self.words.list_names(), len(self.words.sprites()))
                    return 0, self.words.get_order(sprite) * sprite.rect.height
            else:
                return 0, 0  # Sprite() super() adds groups after init, so it doesn't register yet?
        else:

            widths = {word: word.rect.width for word in self.words}  # important to be in order
            # pseduo
            acc = 0
            row = 0
            for word, width in widths.items():
                widths[word] = acc  # x position
                acc += width

                if acc > self.rect.width:
                    print(acc, word.name)

                    widths[word] = 0
                    acc = 0 + width
                    row += 1
                    self.rows.append([])  # new row
                self.rows[-1].append(word)

            self.positions = {word: (widths[word], usefuls.find3d(word, self.rows) * word.rect.height) for word in self.words}

            # print(self.positions[sprite])
            return self.positions[sprite]

class SceneBox(Box):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        super().__init__(rect, 'scene', 'orange', sticky=False, bind=bind)
        self.write_format = True
    def update(self):
        super().update()
        print(self.words.list_names())

class InputBox(Box):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        super().__init__(rect, 'input', 'light blue', sticky=False, bind=bind)
        self.write_format = True


class WordBox(Box):
    def __init__(self, name, color='light green', rect=(0, 0, W, H), bind=None):
        super().__init__(rect, name, color, sticky=True, bind=bind)

print(Interface.instances)
