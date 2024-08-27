import pygame
import re
from button import *
from globs import *
from abstract import *
from usefuls import *

from menu import *


class Word(MySprite):
    words = OrderedGroup()  # needs a new init because ref is too broad
    def __init__(self, string, box):
        """A single word for formatting purposes"""

        super().__init__(string, box, Word.words)

    def default_xy(self):
        return super().default_xy()

    def update(self):
        self.x, self.y = self.default_xy()
        super().update()

    """('Crazy? I was crazy once. They locked me in a room. 
    A rubber room. A rubber room with rats. An rats make me crazy.')"""

class Scene:
    # data-based class, not a sprite, more like a brain
    def __init__(self, words: str, box: WriteBox):
        self.words = words
        self.box = box

    @staticmethod
    def is_key(string) -> "str|bool":
        """Detects if a string is a keyword by <something>"""
        # print(string)
        if not all(x in string for x in ('<', '>')):
            return False
        left = string.index('<')
        right = string.index('>')
        if right >= left:
            return string[left + 1:right]
        return False
        # return string.startswith('<') and string.endswith('>')

    def write(self):
        words = set()
        for i in self.words.split(' '):
            name = self.is_key(i)
            if not name:
                words.add(Word(i, self.box))
            else:  # is keyword
                if name in word_dict.keys():
                    words.add(word_dict[name])  # find the already-made sprite
                else:  # makes a new one
                    words.add(SourceWordBubble(name, cat=None))

# try xml, research
#...add as csv ****
# set(dict('word type': [strings]), dict(...), dict(...),...)
make_words = {
    # this is getting too complex and nested
    verb: ({'go',  }, {'eat', 'make', 'give',}),
    noun: ({'me', 'you', 'what', 'this', }, {'pickle'}),
}
word_bank = {SourceWordBubble(i, cat)   # if True else
             for cat, *val in make_words.items()
             for start, sups in val
             for i in start | sups}
word_dict = {sprite.name: sprite for sprite in word_bank}

for s, *_ in make_words.values():
    for i in s:
        word_dict[i].spawn(None)

MAP = [Scene("It seems that you are in a <pickle>...", box=scene_box)]


class Parser:
    def __init__(self, *words):
        self.words = words

        print(self.words)


class Quest:
    def __init__(self, *words, name, desc):
        self.name = name
        self.desc = desc
        self.words = words

