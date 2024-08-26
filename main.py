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

BACKGROUND = pygame.Surface((W, H))
BACKGROUND.fill('pink')

ok_button = OKButton(usefuls.input_box, menu)

utilities = pygame.sprite.Group()
mymouse = usefuls.MyMouse(utilities)

make_command = pygame.event.custom_type()
# new_command = pygame.event.custom_type()
MAP[0].write()

ticks = 0
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
                if button.hovering and button.visible:  # there will be a 1-tick delay because not updated()
                    # print(button)
                    button.add(clicking)
                    button.set_click(True)
                    button.dirty = 1

        if event.type == pygame.MOUSEBUTTONUP:
            for button in Button.buttons:  # every button is set to False
                button.set_click(False)
                clicking.empty()
                button.dirty = 1

        if pygame.event.get(message_ok):
            # print('', input_box.words.list_names())
            inpt = []
            for bubble in usefuls.input_box.words.sprite_list:
                # print(bubble)
                if type(bubble) is WordBubble:
                    inpt.append(bubble.name)

            Parser(*inpt)

    usefuls.MOUSEPRESSED = pygame.mouse.get_pressed()[0]  # until mousebutton up
    usefuls.MOUSEPOSITION = pygame.mouse.get_pos()
    usefuls.MOUSEREL = pygame.mouse.get_rel()
    mymouse.set_coords(*usefuls.MOUSEPOSITION)  # reason mouse does not update unless moved

    ALLSPRITES.update()


    utilities.update()

    """Drawing """
    ALLSPRITES.clear(SCREEN, BACKGROUND)
    dirty_rects = ALLSPRITES.draw(SCREEN)

    utilities.draw(SCREEN)

    pygame.display.update(dirty_rects)
    # pygame.display.flip()
    CLOCK.tick(60)


print('Goodbye!')
