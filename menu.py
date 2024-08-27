import pygame
from globs import *

from abstract import *

# import usefuls

# pygame.font.init()

# What is the difference between Interface and Box??
# Interfaces can be groups for boxes
class Interface(Thing):
    instances = OrderedGroup()
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

    def update(self):
        super().update()
        # self.items.update()

    def get_rect(self, box):
        # I forgot what this does. Related to param bind?
        try:

            # print(box.name, self.items.get_order(box))
            return pygame.Rect(self.rect.x + self.items.get_order(box) * (self.rect.width / len(self.items)),
                               self.rect.y, int(self.rect.width / len(self.items)), self.rect.height)
        except ValueError:
            raise ValueError


class Box(Interface):

    def __init__(self, rect=(0, 0, W, H), name=None, color='orange',
                 sticky: bool =True, bind: Interface =None, weight:float =1):
        """
        :param sticky: Removing a word does not affect positions
        :param bind: Interface(), overrides self.rect
        """

        self.words = OrderedGroup(name)  # made of Word()s
        self.bind = bind

        super().__init__(rect, name, color)
        print(Interface.instances.list_names())
        self.sticky = sticky  # for non-text boxes

        self.rows = [[]]
        self.positions = {}

        # self.update()

    def update(self):

        super().update()

        if type(self.bind) is Interface:
            self.add(self.bind.items)  # must be phrased to activate OrderedGroup.add_internal()
            self.rect = self.bind.get_rect(self)

        # print(self.words.list_names())
        # print('updating')
        # self.words.update()

    def get_index(self, sprite: MySprite):
        """Returns coords. Calc'd based off other sprites in box.
        Sticky list sprites always have the same place.
        """
        if not sprite in self.words:  # should filter??
            # print('not found', sprite.name)
            return 0, 0
        # print(sprite.name, 'in', self.name)

        if len(self.words) > 0:

            if not self.sticky:
                return 0, self.words.list_names().index(sprite.name) * sprite.rect.height
            else:
                # print(self.words.name, sprite.string, self.words.list_names(), len(self.words.sprites()))
                return 0, self.words.get_order(sprite) * sprite.rect.height
        else:
            return 0, 0  # Sprite() super() adds groups after init, so it doesn't register yet?


class WriteBox(Box, ABC):
    def __init__(self, name, rect=(0, 0, W, H), bind=None):
        super().__init__(rect, name, 'white', sticky=False, bind=bind)

    def get_index(self, sprite: MySprite):
        # print(sprite.name, 'in', self.name)
        # print(sprite in self.words)
        if sprite not in self.words:
            return 0, 0

        widths = {word: word.rect.width for word in self.words}  # important to be in order
        acc = 0
        row = 0
        # print(self.words.list_names())
        for word, width in widths.items():
            widths[word] = acc  # x position
            acc += width
            if acc > self.rect.width:
                widths[word] = 0
                acc = 0 + width
                row += 1
                self.rows.append([])  # new row
            self.rows[-1].append(word)
        self.positions = {word: (widths[word], find3d(word, self.rows) * word.rect.height)
                          for word in self.words}
        return self.positions[sprite]


class SceneBox(WriteBox):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        super().__init__('scene', rect, bind)
        self.color = 'orange'


class InputBox(WriteBox):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        super().__init__('input', rect, bind)
        self.color = 'light blue'

    # def update(self):
    #     super().update()
        # print(self.words.list_names())


class WordBox(Box):
    def __init__(self, name, color='light green', rect=(0, 0, W, H), bind=None):
        super().__init__(rect, name, color, sticky=True, bind=bind)

        self.whitelist = self.words.copy()
    # def update(self):
    #     super().update()
    #     for sprite in self.words:
    #         if not self.whitelist.has(sprite):
    #             self.words.remove(sprite)



