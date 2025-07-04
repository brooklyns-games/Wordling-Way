from pydoc import plain

import pygame

from abstract import Thing

from menu import *


class MyMouse(Thing):
    def __init__(self, *groups):
        super().__init__('mouse', (0, 0, 50, 50), *groups)

        self.font = self.set_font_size(50)

        self.rect = self.image.get_rect()
        self.coords = []

        self.display = False

    def click(self):
        self.coords.append((self.x, self.y))
        if self.display:
            print(self.coords)
            # print((self.x, self.y))

    def draw_me(self):
        self.image = self.font.render('({}, {})'.format(self.x, self.y), True, 'blue')
        return self.image

    def set_coords(self, x, y):
        self.x, self.y = x, y

    def update(self):
        super().update()
        self.dirty = 1


class MyEvent:
    def __init__(self, t:"Callable|int", dic):
        """
        Allows developer to insert events into game, for testing purposes
        :param t: int() that is pygame event type, or func object
        :param dic: attributes to put into t
        """
        self.t = t
        self.dic = dic

    def post(self):
        if self.t in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.mouse):
            if not pygame.mouse.get_focused():
                print('Mouse is not in window')
        if type(self.t) is int:
            self.dic['command'] = True  # new event attr to signal it's a Dev-gen'd event
            pygame.event.post(pygame.event.Event(self.t, self.dic))
        elif callable(self.t):
            # print('callable', self.t)
            if type(self.dic) is dict:
                self.t(**self.dic)
            else:
                self.t(self.dic)

utilities = pygame.sprite.Group()
MYMOUSE = MyMouse(utilities)
message_ok = pygame.USEREVENT + 1

COMMANDS = [
    MyEvent(pygame.MOUSEBUTTONUP, {})
]
plain_mouse_check = [(61, 512),
               (62, 573), (35, 629), (28, 679), (653, 498), (664, 568), (627, 633),
               (645, 684), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (44, 502),
               (44, 502), (55, 556), (41, 634), (29, 677), (630, 506), (645, 576), (642, 637), (664, 678),
               (1126, 441)]
this_bug = [(506, 20)]
pickle = [(471, 26), (471, 26)]

which = plain_mouse_check
for coords in which:
    COMMANDS += [MyEvent(pygame.MOUSEMOTION, {'pos': coords}),  # MyEvent(pygame.mouse.set_pos, coords),
                 MyEvent(pygame.MOUSEBUTTONDOWN, {}),
                 MyEvent(pygame.MOUSEBUTTONUP, {})]
MODE = False
# False to run commands

MOUSEPRESSED = None  # until mousebutton up
MOUSEPOSITION = (0, 0)
MOUSEREL = None

scene_box = SceneBox((0, 0, W, H / 3))
input_box = InputBox([0, H / 3, W, H / 3, ])

wordboxes = Interface([0, int(H * 2 / 3), W, (H / 3)], name='word boxes')
verb = LibraryBox('verb', 'light green', bind=wordboxes)  # optimize calculations
noun = LibraryBox('noun', 'magenta', bind=wordboxes)

all_vars = dir()
for name in all_vars:
    if not name.startswith('__'):
        val = eval(name)
        print(name, ':', val)

mouse_hover = pygame.sprite.Group()
