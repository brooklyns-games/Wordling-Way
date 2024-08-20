import pygame
from globs import *
from words import *
from abstract import OrderedGroup, MySprite, Thing

# pygame.font.init()


class Interface(pygame.sprite.Sprite):
    instances = pygame.sprite.Group()
    def __init__(self, rect=(0, 0, W, H), name=None, color='light blue'):
        # todo adding to Interface.instances also adds to Buttons.instances
        super().__init__(Interface.instances)
        # print('interface', name, len(self.groups()))
        self.name = name  # for developer reference
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)
        self.color = color

        self.mini_rect = self.rect.copy()

        self.items = OrderedGroup()  # other things that are not Word()s


    def draw_me(self):
        self.mini_rect = self.rect.inflate(-50, -50)  # padding
        self.mini_rect = pygame.draw.rect(self.image, self.color,
                                          [(25, 25), self.mini_rect.size])

    def update(self):
        self.draw_me()

    def get_rect(self, box):
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
        self.word_list = []  # list of strings, in order. *All unique.
        self.bind = bind

        super().__init__(rect, name, color)

        self.sticky = sticky

        self.update()

    def update(self):
        super().update()
        try:
            # word_list is dependent on self.words
            self.word_list = list(i.name for i in self.words.sprites())  # redundancy with orderedgroup
        except TypeError:
            raise TypeError

        if type(self.bind) is Interface:
            self.add(self.bind.items)  # must be phrased to activate OrderedGroup.add_internal()
            self.rect = self.bind.get_rect(self)

    def get_index(self, sprite):
        """Returns where the sprite is inside the group. Sticky list sprites always have the same place."""
        self.update()  # words_list and words must sync!

        if len(self.words) > 0:
            if not self.sticky:
                return self.word_list.index(sprite.name)
            else:
                # print(self.words.name, sprite.string, self.words.list_names(), len(self.words.sprites()))
                return self.words.get_order(sprite)
        else:
            return 0  # Sprite() super() adds groups after init, so it doesn't register yet?


class InputBox(Box):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        super().__init__(rect, 'input', 'light blue', sticky=False, bind=bind)


class WordBox(Box):
    def __init__(self, name, color='light green', rect=(0, 0, W, H), bind=None):
        super().__init__(rect, name, color, sticky=True, bind=bind)


