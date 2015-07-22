__author__ = 'zz'
from email.feedparser import BufferedSubFile
import re
from itertools import zip_longest


sep = re.compile(r'(\r\n|\r|\n)')


def py3_splitlines(s):
    split_group = sep.split(s)
    return [g1 + g2 for g1, g2 in zip_longest(split_group[::2], split_group[1::2], fillvalue='')]


# monkey patch the push method
def push(self, data):
    """Push some new data into this object."""
    # Crack into lines, but preserve the linesep characters on the end of each

    # parts = data.splitlines(True)
    # use py3_splitlines instead of the str.splitlines
    parts = py3_splitlines(data)

    if not parts or not parts[0].endswith(('\n', '\r')):
        # No new complete lines, so just accumulate partials
        self._partial += parts
        return

    if self._partial:
        # If there are previous leftovers, complete them now
        self._partial.append(parts[0])
        # and here
        parts[0:1] = py3_splitlines(''.join(self._partial))
        del self._partial[:]

    # If the last element of the list does not end in a newline, then treat
    # it as a partial line.  We only check for '\n' here because a line
    # ending with '\r' might be a line that was split in the middle of a
    # '\r\n' sequence (see bugs 1555570 and 1721862).
    if not parts[-1].endswith('\n'):
        self._partial = [parts.pop()]
    self.pushlines(parts)


def make_fix_splitlines():
    BufferedSubFile.push = push
