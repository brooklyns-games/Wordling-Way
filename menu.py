import pygame
from globs import *

from abstract import *

from button import *

class Interface(Box):
    instances = OrderedGroup()
    def __init__(self, rect=(0, 0, W, H), name=None, color='light blue'):
        super().__init__(name, rect, color=color, )
        self.mini_rect = self.rect.copy()


class WordBox(Box, ABC):
    def __init__(self, name, rect=(0, 0, W, H), bind=None, color='green', include=None):
        """WordBox is an abstract class for the boxes with words in them. """
        # from words import Word
        # from button import WordBubble
        super().__init__(name, rect, color=color, sticky=False, bind=bind, include=include)
        self.rows = [[]]  # facsimile rep of word rows on screen

    def get_index(self, sprite: MySprite):
        from button import OKButton  # todo find better solution
        # print(self.words.list_names())
        # todo remove OK button--in button's init or here?
        # {Sprite: width int}
        widths = {word: word.rect.width for word in self.words
                  }  # important to be in order
        if not self.words.has(sprite):
            return 0, 0

        acc = 0
        row = 0
        for word, width in widths.items():
            if acc > self.rect.width:
                widths[word] = 0  # value = 0
                acc = 0 + width  # move to right
                row += 1
                self.rows.append([])  # new row
            else:
                widths[word] = acc  # value = x position
                acc += width  # moves to right
            self.rows[-1].append(word)  # update self.rows with new data
        # {sprite: (x, y)}
        self.positions = {word: (widths[word], find3d(word, self.rows) * word.rect.height)
                          for word in self.words}
        return self.positions[sprite]


class SceneBox(WordBox):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        """Scene Box is where the narrator explains the scene, and can give you new words"""
        super().__init__('scene', rect, bind, color='orange')


class InputBox(WordBox):
    def __init__(self, rect=(0, 0, W, H), bind=None):
        """Input box is where the user can interact with the scene"""
        super().__init__('input', rect, bind, color='light blue', include=WordBubble)
        self.words = UnorderedGroup(self.name, include=WordBubble)  # recast as Unordered

    # def update(self):
    #     super().update()
        # print(self.words.list_names())


class LibraryBox(Box):
    def __init__(self, name, color='light green', rect=(0, 0, W, H), bind=None):
        """Word box is where you find nouns, verbs, and adjectives"""
        super().__init__(name, rect, color, sticky=True, bind=bind)



