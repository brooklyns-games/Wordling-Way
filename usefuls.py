import pygame

from abstract import Thing

class MyMouse(Thing):
    def __init__(self, *groups):
        super().__init__('mouse', (0, 0, 50, 50), *groups)

        self.font = self.set_font_size(50)

        self.rect = self.image.get_rect()
        self.coords = []

    def click(self):
        self.coords.append((self.x, self.y))

    def draw_me(self):
        self.image = self.font.render('({}, {})'.format(self.x, self.y), True, 'blue')

    def set_coords(self, x, y):
        self.x, self.y = x, y

    def update(self):
        self.draw_me()
        self.rect.update([self.x, self.y], self.image.get_size())


class MyEvent:
    def __init__(self, t, dic):
        self.t = t
        self.dic = dic

        # self.event = pygame.event.custom_type(pygame.event.Event(self.t, a='1'))

    def post(self):
        # print('self.t', self.t)
        if type(self.t) in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.mouse):
            if not pygame.mouse.get_focused():
                print('Mouse is not in window')
        if type(self.t) is int:
            self.dic['command'] = True
            pygame.event.post(pygame.event.Event(self.t, self.dic))
        elif callable(self.t):
            # print('callable', self.t)
            if type(self.dic) is dict:
                self.t(**self.dic)
            else:
                self.t(self.dic)

COMMANDS = [
]

for coords in [(61, 512),
               (62, 573), (35, 629), (28, 679), (653, 498), (664, 568), (627, 633),
               (645, 684), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (51, 28), (44, 502),
               (44, 502), (55, 556), (41, 634), (29, 677), (630, 506), (645, 576), (642, 637), (664, 678),
               (1126, 441)]:
    COMMANDS += [MyEvent(pygame.MOUSEMOTION, {'pos': coords}),  # MyEvent(pygame.mouse.set_pos, coords),
                 MyEvent(pygame.MOUSEBUTTONDOWN, {}),
                 MyEvent(pygame.MOUSEBUTTONUP, {})]

"""
x set visible()
Mouse set_pos()
Mousedown


"""