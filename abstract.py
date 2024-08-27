import pygame

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import *

from globs import *
# from menu import Box

pygame.font.init()

class OrderedGroup(pygame.sprite.AbstractGroup):  # not pygame.sprite.Group
    def __init__(self, name=str(), keep_order=True):  # name == developer reference only
        super().__init__()
        self.sprite_list = list()
        self.name = name  # printin

        self.keep_order = keep_order

    def add_internal(self, sprite:pygame.sprite.Sprite.__subclasses__(), layer=None):
        super().add_internal(sprite)
        if sprite not in self.sprite_list:
            self.sprite_list.append(sprite)

    def remove_internal(self, sprite):
        super().add_internal(sprite)
        if not self.keep_order:
            if sprite in self.sprite_list:
                self.sprite_list.remove(sprite)

    def list_names(self):  #  __str__?
        return list(i.name for i in self.sprite_list)

    def get_order(self, sprite:pygame.sprite.Sprite.__subclasses__()):
        # print(self.name, sprite.string, len(self), self.has(sprite))
        order = dict(enumerate(self.sprite_list))
        reverse_order = {j: i for i, j in order.items()}
        return reverse_order[sprite]

    # def draw_me(self, surface):
    #     super().draw(surface)


def test_instances(klass):
    # if klass
    print(len(klass.instances), klass.instances.list_names())

def get_transparent_surface(size):
    return pygame.Surface(size, pygame.SRCALPHA, 32)

class Thing(pygame.sprite.DirtySprite, ABC):
    # instances =
    def __init__(self, name: str, rect: "Iterable[int] | pygame.Rect", *groups, color='black'):
        super().__init__(*groups, ALLSPRITES)
        # test_instances(Button)
        self.name = name
        self.rect = pygame.Rect(rect)
        self.x, self.y = self.rect.topleft
        self.image = get_transparent_surface(self.rect.size)

        self.font = self.set_font_size(40)
        self.color = color

        # self.update()
        self.dirty = 1

    def set_font_size(self, size: int):
        """I can't remember font syntax"""
        self.font = pygame.font.SysFont(None, size)
        return self.font

    def update_rect(self):
        self.rect.update([self.x, self.y], self.image.get_size())
        return self.rect

    @abstractmethod
    def draw_me(self):
        pass

    def draw_text(self, surface: "tuple(int, int)|pygame.Surface", fit=False):
        text = self.font.render(self.name, True, self.color)
        if type(surface) is not pygame.Surface:
            surface = pygame.Surface(surface)
        surface.blit(text, text.get_rect())

        return surface.copy()

    def update(self):
        self.image = self.draw_me()
        self.update_rect()

        # self.dirty = 1

class Box(Thing, ABC):
    instances = OrderedGroup()
    def __init__(self, name=None, rect=(0, 0, W, H), color='orange',
                 sticky: bool =True, bind=None, weight:float =1):
        """
        :param sticky: Removing a word does not affect positions
        :param bind: Interface(), overrides self.rect
        """

        self.words = OrderedGroup(name)  # made of Word()s
        self.bind = bind

        super().__init__(name, rect, color=color)
        self.sticky = sticky  # for non-text boxes


        self.positions = {}

        self.items = OrderedGroup()  # other things that are not Word()s

    def draw_me(self):
        # self.mini_rect = self.rect.inflate(-50, -50)  # padding
        # self.mini_rect = pygame.draw.rect(self.image, self.color, [(25, 25), self.rect.size])
        self.image.fill(self.color)
        return self.image

    def get_rect(self, box):
        # Related to param bind?
        try:
            return pygame.Rect(self.rect.x + self.items.get_order(box) * (self.rect.width / len(self.items)),
                               self.rect.y, int(self.rect.width / len(self.items)), self.rect.height)
        except ValueError:
            raise ValueError

    def update(self):
        super().update()
        if type(self.bind) in Box.__subclasses__():
            self.add(self.bind.items)  # must be phrased to activate OrderedGroup.add_internal()
            self.rect = self.bind.get_rect(self)  # should override rect


    # todo move somewhere else
    def get_index(self, sprite):
        """Returns coords. Calc'd based off other sprites in box.
        Sticky list sprites always have the same place.
        """
        if len(self.words) > 0 and sprite in self.words:
            if not self.sticky:
                return 0, self.words.list_names().index(sprite.name) * sprite.rect.height
            else:
                # print(self.words.name, sprite.string, self.words.list_names(), len(self.words.sprites()))
                return 0, self.words.get_order(sprite) * sprite.rect.height
        else:
            return 0, 0  # Sprite() super() adds groups after init, so it doesn't register yet?


class MySprite(Thing, ABC):
    # instances = OrderedGroup()  # pygame.sprite.Group()

    def __init__(self, name, box: Box, *groups, autospawn:"bool|Box"=True):  # autospawn: "bool|Box"
        """
        :param name: str() text that appears onscreen
        :param box: Box() or Interface() (?) item that it is located
        :param groups:
        """
        self.font = self.set_font_size(60)
        self.rect = pygame.Rect([0, 0], self.font.size(name))
        super().__init__(name, self.rect, *groups)
        self.box = box

        self.visible = 0  # Must go before
        if autospawn is not False:  # and Box in type(autospawn).__bases__:
            self.spawn(autospawn)
            # print('spawning into', self.box, self.visible, self.rect)

    def spawn(self, box:Box=None):
        # todo box can be diff from self.box
        self.visible = 1
        self.dirty = 1
        if box in (None, True):
            box = self.box
        box.words.add(self)
        print(box.words.list_names())
    def unspawn(self, box=None):
        self.visible = 0
        self.dirty = 1
        if box is None:
            box = self.box
        box.words.remove(self)

    def draw_me(self) -> pygame.Surface:
        """Surface with text on it"""
        self.image = self.draw_text(self.image)
        return self.image

    def default_xy(self) -> (int, int):
        """This is used by Word(), for paragraph formats"""
        box = self.box.rect
        x, y = box.topleft
        x2, y2 = self.box.get_index(self)
        x += x2
        y += y2
        return x, y

    def on_screen(self, screen):
        return not screen.contains(self.rect)




ALLSPRITES = pygame.sprite.LayeredDirty()






