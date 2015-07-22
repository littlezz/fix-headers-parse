from io import StringIO

__author__ = 'zz'

from email.parser import Parser


def parsestr(self, text, headersonly=False):
    text = text.encode('latin1').decode()
    return self.parse(StringIO(text), headersonly=headersonly)


def make_fix_encoding():
    Parser.parsestr = parsestr
