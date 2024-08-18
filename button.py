import pygame
from abstract import MySprite

menu = pygame.sprite.Group()


class Button(MySprite):
    buttons = pygame.sprite.Group()

    def __init__(self, string, interface, *groups, rect=(0, 0, 100, 50), align='left', mode='toggle'):
        # self.string = string
        super().__init__(string, rect, interface, *groups, interface.items, Button.buttons)  # groups adding
        # self.box = interface
        self.mode = mode
        """modes: toggle, event, slider"""

        # self.rect = pygame.Rect(rect)
        # self.image = self.get_transparent_surface(self.rect.size)

        self.align = align
        # self.x, self.y = 0, 0  # self.default_xy()

        self.color = 'green'

        self.at_mouse = True
        self.state = False
        self.hovering = False
        self.clicked = False

    def draw_me(self):
        self.image = self.get_transparent_surface(self.rect.size)
        # self.image.set_alpha(0)
        pygame.draw.rect(self.image, self.color, self.rect, 5, border_radius=15)

        font = pygame.font.SysFont(None, int(self.rect.height))
        text = font.render(str(self.name), True, self.color)
        self.image.blit(text, text.get_rect())
        return self.image

    def click(self):
        """specific behavior what happen when clicked"""
        if self.mode == 'toggle':
            self.state = not self.state

    def set_click(self, switch):
        """
        Sets self.clicked
        :param switch: what to set self.click to
        :return:
        """
        if switch is True:
            self.clicked = True
        elif switch is None:   # closing????
            self.clicked = not self.clicked

        elif switch is False:
            # print('setting', switch, self.string)
            self.clicked = False

        if self.clicked is True:
            self.click()

    def check_click(self):
        """press == bool, clickable()->self.color str()"""
        self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())  # put in collisions? keep here?
        if self.hovering:
            pygame.mouse.get_rel()  # primes for clicking and staying with mouse
            self.color = 'green'
        else:
            self.color = 'white'

        if self.clicked:
            self.color = 'red'
        return self.color

    def default_xy(self):
        if self.align == 'left':
            return self.x, self.y
        elif self.align == 'right':
            return self.box.rect.width - self.image.get_width(), self.box.rect.height - self.image.get_height()

    def update(self):
        self.check_click()  # pygame.mouse.get_pressed()[0]
        # self.string = str(self.state)
        self.draw_me()
        # Updating rect
        if self.at_mouse and self.clicked:
            x2, y2 = pygame.mouse.get_rel()
            self.x += x2
            self.y += y2
        else:
            self.x, self.y = self.default_xy()

        # print(self.rect, type(self.rect))
        self.rect.update([self.x, self.y], self.image.get_size())


class OKButton(Button):
    def __init__(self, interface, *groups):
        super().__init__('OK ->', interface, *groups, align='right', mode='event')
        self.at_mouse = False

    def click(self):
        pygame.event.post(message_ok)

        for sprite in self.box.words.sprites():
            sprite.toggle_box()

    def set_click(self, switch):
        super().set_click(switch)


message_ok = pygame.event.Event(pygame.USEREVENT + 1)

clicking = pygame.sprite.GroupSingle()
