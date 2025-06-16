import pygame
import re

from globs import *
from abstract import *
import usefuls

from button import SourceWordBubble

from pprint import pprint

make_words = {
        # this is getting too complex and nested
        usefuls.verb: ({'look at'}, {'go', 'eat', 'make', 'give', }),
        usefuls.noun: ({'me', 'you', 'what', 'this', }, {'pickle'}),
    }
word_bank = {SourceWordBubble(i, cat, cat=cat, autospawn=False)  # if True else
             for cat, *val in make_words.items()
             for start, sups in val
             for i in start | sups}

# print('words ;3')
word_bank_names = set()
for word in word_bank:
    word_bank_names.add(word.string)

class Word(MySprite):
    words = OrderedGroup()  # needs a new init because ref is too broad
    def __init__(self, string, box):
        """A single word for formatting purposes"""

        super().__init__(string, box, Word.words)

    # def default_xy(self):  # keep
    #     return super().default_xy()

    def update(self):
        self.x, self.y = self.default_xy()
        super().update()

    """('Crazy? I was crazy once. They locked me in a room. 
    A rubber room. A rubber room with rats. An rats make me crazy.')"""

class Scene:

    word_dict = {sprite.name: sprite for sprite in word_bank}

    # data-based class, not a sprite, more like a brain
    def __init__(self, words: str, box: Box):
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
        from button import SourceWordBubble
        words = set()
        for i in self.words.split(' '):
            name = self.is_key(i)

            if not name:
                words.add(Word(i, self.box))
            else:  # detects a keyword
                from usefuls import input_box
                # if name in word_bank_names:
                #     # print(Scene.word_dict[name].make_child(self.box, cls=SourceWordBubble))  # another source
                #     words.add(Scene.word_dict[name])  # find the already-made sprite
                #     print(Scene.word_dict[name].name)
                # else:  # makes a new one
                new_word = SourceWordBubble(name, self.box, cat=input_box, autospawn=True)
                # print(new_word)
                words.add(new_word)

# try xml, research
#...add as csv ****
# set(dict('word type': [strings]), dict(...), dict(...),...)






class Parser:
    def __init__(self, *words):
        self.words = words

        # print(self.words)


class Quest:
    def __init__(self, *words, name, desc):
        self.name = name
        self.desc = desc
        self.words = words

MAP = [
    Scene("You open your eyes to find yourself on the ground floor of an expansive <library>."
          "", box=usefuls.scene_box)
]
