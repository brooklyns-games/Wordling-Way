import pygame

from typing import Union

from abstract import MySprite, OrderedGroup
from menu import Box, SceneBox, WordBox
import usefuls

menu = pygame.sprite.Group()

class Button(MySprite):
    buttons = OrderedGroup()
    def __init__(self, string, box, *groups, align: str ='left', mode='toggle'):
        super().__init__(string, box, *groups, Button.buttons)  # groups adding
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

    def set_click(self, switch:bool):
        """
        Sets self.clicked
        :param switch: what to set self.click to
        :return:
        """
        self.clicked = switch
        # v some complex toggling stuff
        # if switch is True:
        #     self.clicked = True
        # elif switch is None:   # closing????
        #     self.clicked = not self.clicked
        #
        # elif switch is False:
        #     # print('setting', switch, self.string)
        #     self.clicked = False

        if self.clicked is True:
            self.click()

    def default_xy(self):
        # print('default')
        if self.align == 'left':
            return super().default_xy()
        elif self.align == 'right':
            return self.box.rect.x + self.box.rect.width - self.image.get_width(), self.box.rect.y + self.box.rect.height - self.image.get_height()

    def gotomouse(self):
        get_rel = usefuls.MOUSEREL
        x2, y2 = get_rel
        self.x += x2
        self.y += y2
        self.dirty = 1

    # todo move to usefuls
    def check_updates(self):
        """Check if hovering state changes--start or stop hovering"""
        self.hov = self.hovering
        self.hovering = self.rect.collidepoint(*usefuls.MOUSEPOSITION)  # put in collisions? keep here?
        # if self.hov != self.hovering:
        #     print(True, self.hovering, self.clicked)
        return not self.hov == self.hovering

    def update(self):
        if not self.visible:  # saving proc power?
            # self.dirty = 1
            return
        if self.check_updates():
            self.dirty = 1

        if self.hovering:
            pygame.mouse.get_rel()  # primes staying with mouse--assign to 0, 0?? **
            self.color = 'green'
            self.dirty = 1
        elif self.at_mouse and self.clicked:  # clicked also dep on self.hovering
            # print('clicking')
            self.color = 'red'
            self.gotomouse()
            self.dirty = 1
        else:
            self.color = 'white'
            self.x, self.y = self.default_xy()


        # self.dirty = 1

        super().update()  # calls default xy


class WordBubble(Button):
    def __init__(self, string, cat: Union[str, WordBox]=None, autospawn: Union[bool, Box]=False):
        """
        Basic version of wordbubble
        :param cat: Defaults to word_box
        :param spawn:
        """
        super().__init__(string, cat, mode='event', )  # this adds to self.box.items
        # self.word_box = self.box
        self.input_box = usefuls.input_box
        self.cat = cat

        # self.available_boxes = (self.word_box, input_box)  # idk if this can be used
        self.no_repeats = False

        self.visible = 0

        if autospawn is not False:  # and Box in type(autospawn).__bases__:
            # print('spawning into', autospawn.name)
            self.spawn(autospawn)

    def spawn(self, box=None):
        self.visible = 1
        self.dirty = 1
        if box is None:
            box = self.cat
        # print('spawning at', box.name)
        box.words.add(self)
        # print(self.name, self.visible, self.rect)
        print(box.words.list_names())
        # self.update()

    def move_boxes(self):
        pass

    def set_click(self, switch):
        # what?????
        super().set_click(switch)
        if not switch:
            self.state = False
    def click(self):
        # print('click')
        self.toggle_box()

    def toggle_box(self):
        self.box.words.remove(self)
        # print(self.box.words.has(self))
        if self.no_repeats:

            self.input_box.words.add(self)

class SourceWordBubble(WordBubble):
    def __init__(self, string, cat: Union[str, WordBox]=None,):
        super().__init__(string, cat,)

    def make_child(self, dest, cls=WordBubble):
        new = cls(self.name, dest, autospawn=dest)
        # print(new.name, new.visible)
        # new.spawn(dest)
        # new.update()
        # print(new.name, new.visible)
        # print('\t', dest.name)
        # print('\t', dest.words.has(new))

        # print(new.box.name, dest.name)
        return new

    def toggle_box(self):
        """switches between default box and input box. adds 1 self """
        # print('toggle')
        if type(self.box) is SceneBox:
            # print(self.cat.words.list_names(), self.input_box.name)
            if self.name in self.cat.words.list_names():  # word is already there
                self.make_child(self.input_box)
            else:
                self.make_child(self.cat, SourceWordBubble)
        else:
            # print(self.input_box.name)
            self.make_child(self.input_box)

        return self.box


class OKButton(Button):
    def __init__(self, interface, *groups):
        super().__init__('OK ->', interface, *groups, align='right', mode='event')
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
