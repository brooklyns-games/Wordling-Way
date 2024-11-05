import pygame

from abstract import *
from globs import *
from words import Parser, Scene, make_words, MAP
from button import *
# from menu import *

import usefuls

pygame.init()

objectives = {()}

SCREEN = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()

BACKGROUND = pygame.Surface((W, H))
BACKGROUND.fill('pink')

menu = pygame.sprite.Group()
OKBUTTON = OKButton(usefuls.input_box, menu)

make_command = pygame.event.custom_type()

for s, *_ in make_words.values():
    for i in s:
        Scene.word_dict[i].spawn(None)
MAP[0].write()

ticks = 0
done = False
while not done:
    pygame.event.post(pygame.event.Event(make_command))  # each run checks
    if pygame.event.get(make_command) and ticks < len(usefuls.COMMANDS):  # (pygame.time.get_ticks() % 100) < 500 < abs(pygame.time.get_ticks() - tick_range):
        if usefuls.MODE is False:
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
            usefuls.MYMOUSE.click()
            for button in Button.buttons:
                # todo hovered buttons are added to a group, look at group
                if button.hovering and button.visible:  # there will be a 1-tick delay because not updated()
                    # button.add(clicking)
                    button.set_click(True)

        if event.type == pygame.MOUSEBUTTONUP:
            for button in Button.buttons:  # every button is set to False
                button.set_click(False)
                # clicking.empty()

        if pygame.event.get(usefuls.message_ok):
            inpt = []
            for bubble in usefuls.input_box.words.sprite_list:
                # print(bubble)
                if type(bubble) is WordBubble:
                    inpt.append(bubble.name)

            Parser(*inpt)
    """Every-tick updates"""
    usefuls.MOUSEPRESSED = pygame.mouse.get_pressed()[0]  # until mousebutton up
    usefuls.MOUSEPOSITION = pygame.mouse.get_pos()
    usefuls.MOUSEREL = pygame.mouse.get_rel()
    usefuls.MYMOUSE.set_coords(*usefuls.MOUSEPOSITION)  # reason mouse does not update unless moved

    for sprite in usefuls.ALLSPRITES:
        if sprite.rect.collidepoint(*usefuls.MOUSEPOSITION) and pygame.mouse.get_focused():
            pass
    """Sprite updates"""
    usefuls.ALLSPRITES.update()
    usefuls.utilities.update()

    """Drawing """
    ALLSPRITES.clear(SCREEN, BACKGROUND)

    dirty_rects = ALLSPRITES.draw(SCREEN)
    usefuls.utilities.draw(SCREEN)

    pygame.display.update(dirty_rects)
    CLOCK.tick(60)


print('Goodbye!')
