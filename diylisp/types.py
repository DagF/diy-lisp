# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""


class LispError(Exception):
    """General lisp error class."""
    pass


class Closure:
    def __init__(self, env, params, body):
        if not isinstance(params, list):
            raise LispError

        self.env = env
        self.params = params
        self.body = body

    def __repr__(self):
        return "<closure/%d>" % len(self.params)


class Environment:
    def __init__(self, variables=None):
        self.bindings = variables if variables else {}

    def lookup(self, symbol):
        var = self.bindings.get(symbol)
        if var:
            return var
        else:
            raise LispError(symbol)

    def extend(self, variables):
        new_env = Environment(self.bindings.copy())
        new_env.bindings.update(variables)
        return new_env

    def set(self, symbol, value):
        if not self.bindings.get(symbol):
            self.bindings[symbol] = value
        else:
            raise LispError("already defined")


class String:
    """
    Simple data object for representing Lisp strings.

    Ignore this until you start working on part 8.
    """

    def __init__(self, val=""):
        self.val = val

    def __str__(self):
        return '"{}"'.format(self.val)

    def __eq__(self, other):
        return isinstance(other, String) and other.val == self.val
