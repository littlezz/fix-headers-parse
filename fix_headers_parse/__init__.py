__author__ = 'zz'

# from .fix_encoding import make_fix_encoding
# from .fix_splitlines import make_fix_splitlines


_all_fix = ('fix_encoding', 'fix_splitlines')


def _redirect_name(name):
    return 'make_' + name


def make_headers_fix(fix_names=None):
    from .fix_encoding import make_fix_encoding
    from .fix_splitlines import make_fix_splitlines

    if fix_names is None:
        fix_names = _all_fix

    for name in fix_names:
        locals()[_redirect_name(name)]()





