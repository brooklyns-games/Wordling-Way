import pygame
from abstract import MySprite, OrderedGroup

menu = pygame.sprite.Group()

class Button(MySprite):
    buttons = OrderedGroup()
    def __init__(self, string, interface, *groups, align='left', mode='toggle'):
        super().__init__(string, interface, *groups, Button.buttons, rect=(0, 0, 100, 50))  # groups adding
        self.font = self.set_font_size(int(self.rect.height * 1.5))

        self.mode = mode  # modes: toggle, event, slider"""
        self.at_mouse = True
        self.align = align

        self.state = False
        self.hovering = False
        self.clicked = False

    def draw_me(self):
        self.image = self.draw_text(self.image)
        pygame.draw.rect(self.image, self.color, self.rect, 5, border_radius=15)
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
            # print('button default xy', super().default_xy())
            return super().default_xy()
        elif self.align == 'right':
            return self.box.rect.x + self.box.rect.width - self.image.get_width(), self.box.rect.y + self.box.rect.height - self.image.get_height()

    def update(self):
        # super().update()
        self.check_click()  # pygame.mouse.get_pressed()[0]
        # Updating rect
        if self.at_mouse and self.clicked:
            x2, y2 = pygame.mouse.get_rel()
            self.x += x2
            self.y += y2
        else:
            self.x, self.y = self.default_xy()
        super().update()


class WordBubble(Button):
    def __init__(self, string, word_box, input_box):
        # print(string, word_box.words)
        # print(self.box.words)
        # self.string = string
        super().__init__(string, word_box, mode='event')  # this adds to self.box.items
        # Word.__init__(self, string, word_box)
        # For initialization
        self.word_box = self.box
        self.input_box = input_box
        self.available_boxes = (self.word_box, input_box)  # idk if this can be used

    def toggle_box(self):
        """switches between default box and input box. adds 1 self """
        # print('toggling')
        other = None
        if self.box == self.word_box:
            other = self.input_box
        elif self.box == self.input_box:
            other = self.word_box
        else:
            raise ValueError

        self.box.words.remove(self)
        other.words.add(self)  # chill

        self.box = other  # the switch

        self.update_index()  # update all boxes .words?

        return self.box

    def set_click(self, switch):
        super().set_click(switch)
        if not switch:
            self.state = False

    def click(self):
        if not self.state:
            # print('toggle', self.clicked, self.state)
            self.toggle_box()
            self.state = True

    # def update_rect(self):
    #     pass

        # pygame.draw.rect(self.image, self.color, ([0, 0], self.image.get_size()), 5, border_radius=15)

    def update(self):
        # print(self.box)
        super().update()


class OKButton(Button):
    def __init__(self, interface, *groups):
        super().__init__('OK ->', interface, *groups, align='right', mode='event')
        self.at_mouse = False

    def click(self):
        # print('clicked')
        pygame.event.post(pygame.event.Event(message_ok))

        for sprite in self.box.words.sprites():
            if type(sprite) is WordBubble:
                sprite.toggle_box()

    def set_click(self, switch):
        super().set_click(switch)



message_ok = pygame.USEREVENT + 1

clicking = pygame.sprite.GroupSingle()
