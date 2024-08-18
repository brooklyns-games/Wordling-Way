import pygame

from globs import *
from words import *
from button import *
from menu import *

pygame.init()




objectives = {()}

SCREEN = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()

input_box = InputBox([0, 0, W, H * 2 / 3, ])

wordboxes = Interface([0, int(H * 2 / 3), W, (H / 3)], name='word boxes')
verb = WordBox('verb', 'light green', bind=wordboxes)  # optimize calculations
noun = WordBox('noun', 'magenta', bind=wordboxes)
# [W/2, int(H * 2 / 3), W / 2, (H / 3)]
# [0, int(H * 2 / 3), W / 2, (H / 3)],


#...add as csv ****
# set(dict('word type': [strings]), dict(...), dict(...),...)
make_words = {
    verb: {'go', 'eat', 'make', 'give', },
    noun: {'me', 'you', 'what', 'this'}
}
word_bank = {Word(i, cat, input_box) for cat, val in make_words.items() for i in val}
# test = Word('go', verb)
# ok_button = Button('OK', input_box, menu, rect=(0, 0, 200, 100), align='right')
ok_button = OKButton(input_box, menu)


while True:
    # mouse_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in Button.buttons:
                if button.hovering:  # there will be a 1-tick delay because not updated()

                    button.add(clicking)
                    button.set_click(True)

        if event.type == pygame.MOUSEBUTTONUP:
            for button in Button.buttons:  # every button is set to False
                button.set_click(False)
                clicking.empty()

        if event == message_ok:
            print(input_box.words.list_names())
            Parser(input_box.words.list_names())
    # override :)
    mouse_pressed = pygame.mouse.get_pressed()[0]  # until mousebutton up

    Word.instances.update()
    Box.instances.update()  # which should come first?
    menu.update()  # should go last

    SCREEN.fill('pink')

    # Box.instances.draw(SCREEN)  # boxes
    Interface.instances.draw(SCREEN)  # boxes and menus
    Word.instances.draw(SCREEN)  # words

    menu.draw(SCREEN)

    pygame.display.flip()
    CLOCK.tick(60)
