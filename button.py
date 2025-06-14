# import pygame

from abstract import *
import usefuls


class Button(MySprite):
    buttons = OrderedGroup()
    def __init__(self, string, box, *groups, align:str='left', mode:str='toggle', autospawn=True):
        super().__init__(string, box, *groups, Button.buttons, autospawn=autospawn)  # groups adding
        self.font = self.set_font_size(int(self.rect.height * 1.5))
        self.string = string

        self.mode = mode  # modes: toggle, event, slider"""
        self.clickable = True
        self.align = align

        self.state = False

        self.hovering = False  # bool if mouse is touching sprite
        self.hov = False
        self.clicked = False

        # self.dirty = 2

    def draw_me(self):  # todo see readme
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
        :return: self.hovering
        """
        self.clicked = switch
        if self.clicked is True:
            self.click()
        self.dirty = 1

    def default_xy(self) -> (int, int):
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

    def update(self):
        if not self.visible:  # saving proc power?
            return

        # updates when starts/stops mouse hovering over
        self.hov = self.hovering
        self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hov != self.hovering:
            self.dirty = 1
        # if self.check_updates():
        #     self.dirty = 1
        if self.hovering:
            usefuls.MOUSEREL = (0, 0)  # primes staying with mouse--assign to 0, 0?? **
            self.color = 'green'
            self.dirty = 1
        elif self.clickable and self.clicked:  # clicked also dep on self.hovering
            # print('clicking')
            self.color = 'red'
            self.gotomouse()
            self.dirty = 1
        else:
            self.color = 'white'
            # print(self.default_xy())
            self.x, self.y = self.default_xy()
        # self.dirty = 1
        super().update()  # calls default xy

# from words import Word
class WordBubble(Button):
    def __init__(self, string, box: Union[str, Box]=None, cat:Box=None, autospawn=False):
        """
        Basic version of wordbubble
        :param cat: Defaults to word_box
        :param spawn:
        """
        super().__init__(string, box, mode='event', autospawn=autospawn)  # this adds to self.box.items
        self.input_box = usefuls.input_box
        if type(cat) is None:
            self.cat = self.box
        else:
            self.cat = cat  # same as self.box

        # self.available_boxes = (self.word_box, input_box)  # idk if this can be used
        self.no_repeats = False

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
        self.unspawn(self.box)  # needs to detect which box it's in
        if self.no_repeats:
            self.input_box.words.add(self)
    def update(self):
        super().update()
        # print(self.name, self.box, self.rect, self.visible)

class SourceWordBubble(WordBubble):
    def __init__(self, string, box, cat=None, autospawn=False):
        super().__init__(string, box, cat=cat, autospawn=autospawn)
        print(self.string)

    def make_child(self, dest, cls=WordBubble) -> WordBubble:
        """Creates a new child inside this box"""
        new = cls(self.name, dest, cat=self.cat, autospawn=dest)
        # print(new.box.name, '!', new.box.words.has(new), new.visible)  # this works
        return new

    def toggle_box(self):
        """switches between default box and input box. adds 1 self """
        # print('toggle')
        from menu import SceneBox
        if type(self.box) is SceneBox:  # todo put in method in box, scenebox still does this
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
    def __init__(self, box, *groups):
        """Button for submitting words in Input box"""
        super().__init__('OK ->', None, *groups, align='right', mode='event', autospawn=box)
        self.clickable = True

    def click(self):
        pygame.event.post(pygame.event.Event(usefuls.message_ok))

        for sprite in self.box.words.sprites():
            if type(sprite) is WordBubble:
                sprite.toggle_box()
