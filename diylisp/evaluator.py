# -*- coding: utf-8 -*-

from .types import Environment, LispError, Closure, String
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer, is_string
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):

    if not is_list(ast):
        if is_boolean(ast):
            return ast
        elif is_integer(ast):
            return ast
        else:
            return env.lookup(ast)

    if len(ast) > 2:
        key, *rest = ast
    else:
        key, rest = ast


    print(ast)
    print(key)
    print(rest)

    if key == 'quote':
        return rest
    elif key == 'atom':
        if is_list(rest):
            res = evaluate(rest, env)
            return False if is_list(res) else True
        else:
            return True

    if is_list(rest) and len(rest) == 2:
        value1, value2 = rest
    else:
        value1, value2 = rest, None
    if is_list(value1):
        value1 = evaluate(value1, env)
    if is_list(value2):
        value2 = evaluate(value2, env)

    if key == 'eq':
        if is_list(value1) or is_list(value2):
            return False
        return value1 == value2

    elif key == "define":
        if value2:
            if isinstance(value1, str):
                env.set(value1, value2)
            else:
                raise LispError("non-symbol")
        else:
            raise LispError("Wrong number of arguments")


    if key == '+':
        if is_integer(value1) and is_integer(value2):
            return value1 + value2
        else:
            raise LispError

    if key == '-':
        if is_integer(value1) and is_integer(value2):
            return value1 - value2
        else:
            raise LispError

    if key == '/':
        if is_integer(value1) and is_integer(value2):
            return value1 // value2
        else:
            raise LispError

    if key == '*':
        if is_integer(value1) and is_integer(value2):
            return value1 * value2
        else:
            raise LispError

    if key == 'mod':
        if is_integer(value1) and is_integer(value2):
            return value1 % value2
        else:
            raise LispError

    if key == '>':
        if is_integer(value1) and is_integer(value2):
            return value1 > value2
        else:
            raise LispError


    if key == 'if':
        if is_list(rest) and len(rest) == 3:
            predicate, expresion1, expresion2 = rest
            if evaluate(predicate, env):
                return evaluate(expresion1, env)
            else:
                return evaluate(expresion2, env)
        else:
            raise LispError




