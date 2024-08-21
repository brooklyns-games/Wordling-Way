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
    # if klass
    print(len(klass.instances), klass.instances.list_names())


class Thing(pygame.sprite.Sprite, ABC):
    # instances =
    def __init__(self, name, rect, *groups):
        super().__init__(*groups)
        # test_instances(Button)
        self.name = name
        self.rect = pygame.Rect(rect)
        self.x, self.y = self.rect.topleft
        self.image = self.get_transparent_surface(self.rect.size)

        self.font = self.set_font_size(40)

    def get_transparent_surface(self, size):
        return pygame.Surface(size, pygame.SRCALPHA, 32)

    def set_font_size(self, size):
        """I can't remember font syntax"""
        self.font = pygame.font.SysFont(None, size)
        return self.font

    def update_rect(self):
        # print(self.image)
        self.rect.update([self.x, self.y], self.image.get_size())
        return self.rect

    @abstractmethod
    def draw_me(self):
        pass

    # @abstractmethod
    def update(self):
        self.image = self.draw_me()
        self.update_rect()



class MySprite(Thing, ABC):
    # instances = OrderedGroup()  # pygame.sprite.Group()

    def add_instance(self):
        self.__class__.instances = self.__class__.instances.copy()
        self.__class__.instances.add(self)

    def __init__(self, name, box, *groups, rect=(0, 0, 50, 50)):
        from button import Button
        """

        :param name: str() text that appears onscreen
        :param rect:
        :param box: Box() or Interface() (?) item that it is located
        :param groups:
        """
        self.font = self.set_font_size(60)
        self.rect = pygame.Rect([0, 0], self.font.size(name))
        super().__init__(name, self.rect, *groups, box.words, )
        self.box = box
        self.color = 'black'
        self.index = 0

    def draw_text(self, surface, fit=False):
        text = self.font.render(self.name, True, self.color)
        if type(surface) is not pygame.Surface:
            surface = pygame.Surface(surface)
        surface.blit(text, text.get_rect())
        # print('word draw')

        return surface.copy()

    def draw_me(self):
        self.image = self.draw_text(self.image)
        return self.image

    def update_index(self):  # everything is clumped because self.index = 0
        # print('update index', self.__class__, self.box)
        self.index = self.box.get_index(self)
        return self.index

    def default_xy(self):
        # print('default xy')  # does not show

        box = self.box.rect
        # self.update_index() - 0
        # x, y = box.x, (box.y + (self.box.get_index(self)- 0) * 60)  # list format
        x, y = box.topleft
        x2, y2 = self.box.get_index(self)
        x += x2
        y += y2
        return x, y

    def update(self):

        self.x, self.y = self.default_xy()
        super().update()


    # @classmethod
    # def self_group(cls, instance):
    #     # print('\tadding', cls, len(cls.instances))
    #     cls.instances.add(instance)
    #     # print(len(cls.instances))

    def on_screen(self, screen):
        return not screen.contains(self.rect)


# class MyEvent(pygame.event.Event):
#     def __init__(self, t, dic):
#         super().__init__(t, dic)











