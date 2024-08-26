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
        # ! passing box instead of self.box seems to solve everything-is-Button problem

        # print('before word')
        # print(self.__class__.__name__, self.groups())
        # test_instances(Button)
        # Word.instances
        super().__init__(string, box, Word.words)
    def default_xy(self):
        return super().default_xy()

    def update(self):
        # print('sdfdf', self.image)
        self.x, self.y = self.default_xy()
        super().update()

    """('Crazy? I was crazy once. They locked me in a room. 
    A rubber room. A rubber room with rats. An rats make me crazy.')"""

class Scene:
    # data-based class, not a sprite, more like a brain
    def __init__(self, words: str, box: WriteBox):
        self.words = words
        self.box = box

        # keywords = re.findall('^<*>', self.words)  # <*>'
        # print(keywords)

    def is_key(self, string):
        # print(string)
        if not all(x in string for x in ('<', '>')):
            return False
        left = string.index('<')
        right = string.index('>')
        if right >= left:
            # print(string[left + 1:right])
            return string[left + 1:right]
        # return string.startswith('<') and string.endswith('>')

    def write(self):
        words = set()
        for i in self.words.split(' '):
            name = self.is_key(i)
            if not name:
                words.add(Word(i, self.box))
            else:
                if name in word_dict:
                    cat = word_dict[name].cat
                else:
                    cat = None
                words.add(SourceWordBubble(name, self.box, usefuls.input_box, cat=cat))

# try xml, research
#...add as csv ****
# set(dict('word type': [strings]), dict(...), dict(...),...)
make_words = {
    # this is getting too complex and nested
    verb: ({'go',  }, {'eat', 'make', 'give',}),
    noun: ({'me', 'you', 'what', 'this', }, {'pickle'}),
}
word_bank = {SourceWordBubble(i, cat, usefuls.input_box, cat=cat, spawn=i in start)   # if True else
             # WordBubble(i, cat, )
             for cat, *val in make_words.items()
             for start, sups in val
             for i in start | sups}
word_dict = {sprite.name: sprite for sprite in word_bank}
# levels

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

