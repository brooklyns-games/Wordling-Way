import pygame

from typing import Union

from abstract import MySprite, OrderedGroup
from menu import Box, SceneBox, WordBox
import usefuls

menu = pygame.sprite.Group()

class Button(MySprite):
    buttons = OrderedGroup()
    def __init__(self, string, box, *groups, align: str ='left', mode='toggle', spawn=True):
        super().__init__(string, box, *groups, Button.buttons, spawn=spawn)  # groups adding
        # rect=(0, 0, 100, 50)
        # print(string, spawn, self.box.words.list_names())
        self.font = self.set_font_size(int(self.rect.height * 1.5))

        self.mode = mode  # modes: toggle, event, slider"""
        self.at_mouse = True
        self.align = align

        self.state = False

        self.hovering = False
        self.hov = False
        self.clicked = False

    def draw_me(self):
        self.image = self.draw_text(self.image)
        pygame.draw.rect(self.image, self.color, self.rect, 5, border_radius=15)
        return self.image

    def click(self):
        """specific behavior what happen when clicked"""
        if self.mode == 'toggle':
            self.state = not self.state
        # self.dirty = 1

    def set_click(self, switch:bool):
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

    def default_xy(self):
        if self.align == 'left':
            return super().default_xy()
        elif self.align == 'right':
            return self.box.rect.x + self.box.rect.width - self.image.get_width(), self.box.rect.y + self.box.rect.height - self.image.get_height()

    def gotomouse(self):
        get_rel = usefuls.MOUSEREL
        # print(get_rel)
        x2, y2 = get_rel
        self.x += x2
        self.y += y2
        self.dirty = 1

    def check_updates(self):
        """Check if hovering state changes--start or stop hovering"""
        self.hov = self.hovering
        self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())  # put in collisions? keep here?
        # if self.hov != self.hovering:
        #     print('yeet')
        return not self.hov == self.hovering


    def update(self):
        # super().update()
        # print(self.dirty)
        if self.check_updates():
            self.dirty = 1

        self.color = 'white'
        self.x, self.y = self.default_xy()

        if self.hovering:
            pygame.mouse.get_rel()  # primes for clicking and staying with mouse
            # self.dirty = 1
            self.color = 'green'

        if self.at_mouse and self.clicked:
            self.color = 'red'
            self.gotomouse()

        super().update()

# class SourceBubble(WordBubble):
#     pass
class WordBubble(Button):
    def __init__(self, string, word_box, input_box: Box, cat: Union[str, WordBox]=None, spawn=None):
        """

        :param cat: Defaults to word_box
        :param spawn:
        """
        super().__init__(string, word_box, mode='event')  # this adds to self.box.items
        self.word_box = self.box
        self.input_box = input_box

        if cat is None:
            self.cat = word_box
        else:
            self.cat = cat

        self.available_boxes = (self.word_box, input_box)  # idk if this can be used

    def move_boxes(self):
        pass

    def toggle_box(self):
        """switches between default box and input box. adds 1 self """
        # print('toggling')
        if type(self.box) is SceneBox:
            # print(vars(self))
            new = self.__class__(self.name, self.cat, self.input_box, self.cat)
        else:
            if self.box == self.word_box:
                other = self.input_box
            elif self.box == self.input_box:
                other = self.word_box
            else:
                raise ValueError

            # todo reset state??
            self.box.words.remove(self)
            other.words.add(self)  # chill

            self.box = other  # the switch

        # should update in self.update() automatically

        return self.box

    def set_click(self, switch):
        super().set_click(switch)
        if not switch:
            self.state = False

    def click(self):
        if not self.state:  # todo what is self.state in bubble?
            # print('toggle', self.clicked, self.state)
            self.toggle_box()
            self.state = True

    # def update(self):
        # print(self.box)
        # super().update()


class OKButton(Button):
    def __init__(self, interface, *groups):
        super().__init__('OK ->', interface, *groups, align='right', mode='event', spawn=False)
        self.at_mouse = False

        # self.box.words.remove(self)  # to not mess up formatting
        # print(self.box.words.list_names())
        self.box.items.add(self)
        # print(self.box.words.list_names())

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
