import pygame
from abc import ABC, abstractmethod
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
        return str(list(i.name for i in self.sprite_list))

    def get_order(self, sprite):
        # print(self.name, sprite.string, len(self), self.has(sprite))
        order = dict(enumerate(self.sprite_list))
        reverse_order = {j: i for i, j in order.items()}
        return reverse_order[sprite]

def test_instances(klass):
    print(len(klass.instances), klass.instances.list_names())


class Thing(pygame.sprite.Sprite, ABC):
    def __init__(self, name, rect, *groups):
        super().__init__(*groups)
        self.name = name
        self.rect = pygame.Rect(rect)
        self.x, self.y = self.rect.topleft
        self.image = self.get_transparent_surface(self.rect.size)

        self.font = self.set_font_size(80)

    def get_transparent_surface(self, size):
        return pygame.Surface(size, pygame.SRCALPHA, 32)

    def set_font_size(self, size):
        """I can't remember font syntax"""
        self.font = pygame.font.SysFont(None, size)
        return self.font


    @abstractmethod
    def draw_me(self):
        pass

    @abstractmethod
    def update(self):
        self.draw_me()


class MySprite(Thing, ABC):
    instances = OrderedGroup()  # pygame.sprite.Group()

    def __init__(self, name, rect, *groups):
        # print(type(self), name, groups)
        super().__init__(name, rect, *groups, )

        self.font = pygame.font.SysFont(None, 80)

        # self.box = box

    @classmethod
    def self_group(cls, instance):
        # print('\tadding', cls, len(cls.instances))
        cls.instances.add(instance)
        # print(len(cls.instances))

    def on_screen(self, screen):
        return not screen.contains(self.rect)


# class MyEvent(pygame.event.Event):
#     def __init__(self, t, dic):
#         super().__init__(t, dic)











