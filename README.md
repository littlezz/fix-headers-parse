# fix-headers-parse
monkey patch to fix python3 headers parse when headers contain some special character , eg, some chinese 


In python3, the http.client decode headers by 'latin1', which would cause some Chinese characters encode as 'utf8' by server, but
decode as 'latin1' by client, which will contain some special character, for example, '\x85'.

The terrible thing is, in python3, `email.feedparser.BufferedSubFile` split data by `str.splitlines`, which would
split on the  `\x85`. (https://docs.python.org/3.5/library/stdtypes.html#str.splitlines)

This module try to use monkey patch to replace the behave of `push` method in
the `email.feedparser.BufferedSubFile` to avoid headers split by `\x85`



Quick Start
---------------
fix splitlines and encoding

```python
from fix_headers_parse make_headers_fix

make_headers_fix()

```

or just explicit fix 'splitlines'

```python
make_headers_fix('fix_splitlines')
```

here is list of fix:

- fix_splitlines
- fix_encoding

