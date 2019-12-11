# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""The classic ``compose``, with all the Pythonic features."""


__all__ = ('compose',)
__version__ = '1.0.0'


def _name(obj):
    return type(obj).__name__


class compose(object):
    """Function composition: compose(f, g)(...) is equivalent to f(g(...)))

    Arguments:
        *functions: Functions (or other callables) to compose.
            Other instances of `compose` in the arguments are expanded
            into their composed functions instead of nesting.

    Attributes:
        functions: Read-only tuple of the composed functions (in the
            order they will be executed, not in the order passed in).

    Raises:
        TypeError:
            If no arguments are given.
            If any argument is not callable.
    """

    def __init__(self, *functions):
        if not functions:
            name = _name(self)
            raise TypeError(repr(name) + ' needs at least one argument')
        _functions = []
        for function in functions[::-1]:
            if not callable(function):
                name = _name(self)
                raise TypeError(repr(name) + ' arguments must be callable')
            if isinstance(function, compose):
                _functions.extend(function.functions)
            else:
                _functions.append(function)
        self.__wrapped__ = _functions[0]
        self._wrappers = tuple(_functions[1:])

    def __call__(*args, **kwargs):
        self, args = args[0], args[1:]
        result = self.__wrapped__(*args, **kwargs)
        for function in self._wrappers:
            result = function(result)
        return result

    def __repr__(self):
        return _name(self) + repr(self.functions[::-1])

    @property
    def functions(self):
        return (self.__wrapped__,) + self._wrappers


# Portability to some minimal Python implementations:
try:
    compose.__name__
except AttributeError:
    compose.__name__ = 'compose'