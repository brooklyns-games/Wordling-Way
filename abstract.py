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


class MySprite(pygame.sprite.Sprite, ABC):
    instances = OrderedGroup()  # pygame.sprite.Group()

    def __init__(self, name, rect, *groups):
        # print(type(self), name, groups)
        super().__init__(*groups, )
        # self.__class__.instances
        # self.self_group(self)

        self.name = name  # name or string
        self.rect = pygame.Rect(rect)
        self.image = self.get_transparent_surface(self.rect.size)
        self.x, self.y = 0, 0

        self.font = pygame.font.SysFont(None, 80)

        # self.box = box

    @classmethod
    def self_group(cls, instance):
        print('\tadding', cls, len(cls.instances))
        cls.instances.add(instance)
        # print(len(cls.instances))

    def on_screen(self, screen):
        return not screen.contains(self.rect)

    def set_font_size(self, size):
        """I can't remember font syntax"""
        self.font = pygame.font.SysFont(None, size)
        return self.font

    def get_transparent_surface(self, size):
        return pygame.Surface(size, pygame.SRCALPHA, 32)

    @abstractmethod
    def draw_me(self):
        pass

    @abstractmethod
    def update(self):
        self.draw_me()





