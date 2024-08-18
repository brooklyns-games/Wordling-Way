import pygame
from abc import ABC, abstractmethod


class MySprite(pygame.sprite.Sprite, ABC):
    instances = pygame.sprite.Group()

    def __init__(self, name, rect, box, *groups):
        super().__init__(*groups)
        self.name = name  # name or string
        self.rect = pygame.Rect(rect)
        self.image = self.get_transparent_surface(self.rect.size)
        self.x, self.y = 0, 0

        self.box = box

    def get_transparent_surface(self, size):
        return pygame.Surface(size, pygame.SRCALPHA, 32)

    @abstractmethod
    def draw_me(self):
        pass

    @abstractmethod
    def update(self):
        pass



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


