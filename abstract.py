import pygame
from abc import ABC, abstractmethod
from typing import Union
pygame.font.init()

class OrderedGroup(pygame.sprite.AbstractGroup):  # not pygame.sprite.Group
    def __init__(self, name=str()):  # name == developer reference only
        super().__init__()
        self.sprite_list = list()
        self.name = name  # printin

    def add_internal(self, sprite, layer=None):
        super().add_internal(sprite)
        if sprite not in self.sprite_list:
            self.sprite_list.append(sprite)
        # print(self.sprites(), len(self.sprites()) == len(self.sprite_list))

    def list_names(self):  #  __str__?
        return list(i.name for i in self.sprite_list)

    def get_order(self, sprite: pygame.sprite.Sprite):
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
    def __init__(self, name: str, rect: Union[list, tuple, pygame.Rect], *groups):
        super().__init__(*groups, ALLSPRITES)
        # test_instances(Button)
        self.name = name
        self.rect = pygame.Rect(rect)
        self.x, self.y = self.rect.topleft
        self.image = get_transparent_surface(self.rect.size)

        self.font = self.set_font_size(40)
        self.color = 'black'

        # self.update()
        self.dirty = 1

    def set_font_size(self, size):
        """I can't remember font syntax"""
        self.font = pygame.font.SysFont(None, size)
        return self.font

    def update_rect(self):
        self.rect.update([self.x, self.y], self.image.get_size())
        return self.rect

    @abstractmethod
    def draw_me(self):
        pass

    def draw_text(self, surface, fit=False):
        text = self.font.render(self.name, True, self.color)
        if type(surface) is not pygame.Surface:
            surface = pygame.Surface(surface)
        surface.blit(text, text.get_rect())

        return surface.copy()
    # @abstractmethod
    def update(self):
        self.image = self.draw_me()
        self.update_rect()

        # self.dirty = 1


class MySprite(Thing, ABC):
    # instances = OrderedGroup()  # pygame.sprite.Group()

    def __init__(self, name, box, *groups, spawn=True, ):
        rect = (0, 0, 50, 50)
        """

        :param name: str() text that appears onscreen
        :param box: Box() or Interface() (?) item that it is located
        :param groups:
        """
        self.font = self.set_font_size(60)
        self.rect = pygame.Rect([0, 0], self.font.size(name))
        super().__init__(name, self.rect, *groups)

        from menu import SceneBox
        if spawn or type(box) is SceneBox:
            box.words.add(self)
        print(spawn, self.name, type(box))
        self.hide = spawn
            # print('added', self.name)

        self.box = box
        # self.loc = pygame.sprite.GroupSingle(self.box.words)

        self.color = 'black'
        self.index = 0



    def spawn_at(self):
        pass



    def draw_me(self):
        """Surface with text on it"""
        self.image = self.draw_text(self.image)
        return self.image

    def default_xy(self):
        """This is used by Word(), for paragraph formats"""
        box = self.box.rect
        x, y = box.topleft
        x2, y2 = self.box.get_index(self)
        x += x2
        y += y2
        return x, y

    def update(self):
        # self.loc = pygame.sprite.GroupSingle(self.box.words)

        # if self.hide:
        #     self.box.words.sprite.remove(self)  # ?? what is sprite
        # else:
        #     self.box.words.add(self)
        self.visible = self in self.box.words

        # self.x, self.y = self.default_xy()  # the indiv objects might have a different pos
        super().update()
        # self.dirty = 1

    def on_screen(self, screen):
        return not screen.contains(self.rect)


ALLSPRITES = pygame.sprite.LayeredDirty()






