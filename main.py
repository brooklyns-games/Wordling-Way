import pygame

from globs import *
from words import *
from button import *
from menu import *

import usefuls

pygame.init()

objectives = {()}

SCREEN = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()

scene_box = SceneBox((0, 0, W, H / 3))
input_box = InputBox([0, H / 3, W, H / 3, ])

wordboxes = Interface([0, int(H * 2 / 3), W, (H / 3)], name='word boxes')
verb = WordBox('verb', 'light green', bind=wordboxes)  # optimize calculations
noun = WordBox('noun', 'magenta', bind=wordboxes)

print(Interface.instances.sprites())

#...add as csv ****
# set(dict('word type': [strings]), dict(...), dict(...),...)
make_words = {
    verb: {'go', 'eat', 'make', 'give', },
    noun: {'me', 'you', 'what', 'this'}
}
word_bank = {WordBubble(i, cat, input_box) for cat, val in make_words.items() for i in val}
words = {Word(i, scene_box) for i in ('Crazy? I was crazy once. They locked me in a room. '
                                      'A rubber room. A rubber room with rats. An rats make me crazy.').split(' ')}

# test = Word('go', verb)
# ok_button = Button('OK', input_box, menu, rect=(0, 0, 200, 100), align='right')
ok_button = OKButton(input_box, menu)

utilities = pygame.sprite.Group()
mymouse = usefuls.MyMouse(utilities)

make_command = pygame.event.custom_type()
new_command = pygame.event.custom_type()
# pygame.time.set_timer(pygame.event.Event(make_command), int(1000/50), loops=len(usefuls.COMMANDS) - 1)  # extra precaution for index

# pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN])

ticks = 0
tick_range = 0
done = False
while not done:

    # blocked = False
    pygame.event.post(pygame.event.Event(make_command))  # each run checks

    # v delete this?
    if pygame.event.get(make_command):  # (pygame.time.get_ticks() % 100) < 500 < abs(pygame.time.get_ticks() - tick_range):
        if usefuls.MODE is False:
            if ticks < len(usefuls.COMMANDS):
                myevent = usefuls.COMMANDS[ticks]  # at least one tick must go by
                ticks += 1

                pygame.event.clear()
                myevent.post()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        # v distinguishes Command events and User-generated events
        if event.type == pygame.MOUSEMOTION and 'command' in event.__dict__:
            pygame.mouse.set_pos(event.pos)


        if event.type == pygame.MOUSEBUTTONDOWN:
            mymouse.click()
            for button in Button.buttons:
                if button.hovering:  # there will be a 1-tick delay because not updated()
                    # print(button)
                    button.add(clicking)
                    button.set_click(True)

        if event.type == pygame.MOUSEBUTTONUP:
            for button in Button.buttons:  # every button is set to False
                button.set_click(False)
                clicking.empty()

        if pygame.event.get(message_ok):
            # print('', input_box.words.list_names())
            inpt = []
            for bubble in input_box.words.list_names():
                if type(bubble) is WordBubble:
                    inpt.append(bubble)

            Parser(*inpt)

    MOUSEPRESSED = pygame.mouse.get_pressed()[0]  # until mousebutton up
    MOUSEPOSITION = pygame.mouse.get_pos()
    mymouse.set_coords(*MOUSEPOSITION)  # reason mouse does not update unless moved

    Interface.instances.update()
    Button.buttons.update()
    Word.words.update()
    # Box.instances.update()  # which should come first?
    menu.update()  # should go last

    utilities.update()

    SCREEN.fill('pink')
    # Box.instances.draw(SCREEN)  # boxes
    Interface.instances.draw(SCREEN)  # boxes and menus  todo find
    Button.buttons.draw(SCREEN)
    Word.words.draw(SCREEN)
    # WordBubble.instances.draw(SCREEN)  # words
    menu.draw(SCREEN)

    utilities.draw(SCREEN)

    pygame.display.flip()
    # ticks += 1
    CLOCK.tick(60)


print('Goodbye!')
