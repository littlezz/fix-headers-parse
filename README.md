# fix-headers-parse
monkey patch to fix python3 headers parse when headers contain some special character , eg, some chinese 


This module try to use monkey patch to replace the behave of `push` method in
the `email.feedparser.BufferedSubFile` to avoid headers split by `\x85` (fix_splitlines)

And use utf8 to decode the headers (fix_encoding)


Install
------------
You need pip to install this library.

```
pip3 install git+https://github.com/littlezz/fix-headers-parse
```



Quick Start
---------------
fix splitlines and encoding

```python
from fix_headers_parse import make_headers_fix

make_headers_fix()

```

or just explicit fix 'splitlines'


```python
make_headers_fix('fix_splitlines')
```

here is list of fix:

- fix_splitlines
- fix_encoding


Why this library
---------
python3 use latin-1 to decode the headers, if some Chinese encode by utf8, but decode by latin-1,   it may contain `\x85` in the result.

```python
In [276]: '锅团子圣诞树.jpg'.encode('utf8').decode('latin1')
Out[276]: 'é\x94\x85å\x9b¢å\xad\x90å\x9c£è¯\x9eæ\xa0\x91.jpg'

In [278]: '\x85' in '锅团子圣诞树.jpg'.encode('utf8').decode('latin1')
Out[278]: True

```

In `email.feedparser.BufferedSubFile`, the push method split data by  `str.splitlines` , which will split on `\x85`.  (https://docs.python.org/3.5/library/stdtypes.html#str.splitlines)
This will make headers content lost after the `\x85`.

I write a simple server to return Chinese headers encode by utf8.

```python

from flask import Flask, make_response
app = Flask(__name__)


@app.route('/rt')
def rt():
    r = make_response()
    r.headers['chinese-header'] = '锅团子圣诞树.jpg'.encode('utf8')
    return r

if __name__ == '__main__':
    app.run(port=8088, debug=True)
```

and then get it.

```python
In [275]: requests.get('http://127.0.0.1:8088/rt').headers['chinese-header']
Out[275]: 'é\x94\x85'
```

It lost content after `\x85`.

I write a function to replace the `push` method,  it replace the `str.splitlines` to split only on `\r`, `\n`, `\r\n`.

```python
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


BufferedSubFile.push = push
```

after replace the `splitlines` to `py3_splitlines` in `push` method.

```python
In [280]: requests.get('http://127.0.0.1:8088/rt').headers['chinese-header']
Out[280]: 'é\x94\x85å\x9b¢å\xad\x90å\x9c£è¯\x9eæ\xa0\x91.jpg'
```

and then we can re-encode the headers and  get the correct one


So, I think we can use monkey patch to fix the `BufferedSubFile.push` method when people use python3.
I also find that the str.splitlines in `BufferedSubFile.push` may be a bug (http://bugs.python.org/issue22233).
But until now, it seems that python source code doesn't change.
