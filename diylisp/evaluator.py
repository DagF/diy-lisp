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

def eval_quote(rest):
    return rest

def eval_atom(rest,env):
    return is_atom(evaluate(rest,env))

def eval_eq(rest, env):
    val1, val2 = rest
    val1 = evaluate(val1, env)
    val2 = evaluate(val2, env)

    return is_atom(val1) and val1 == val2

def eval_math(key, rest, env):
    val1 = evaluate(rest[0], env)
    val2 = evaluate(rest[1], env)

    if not is_integer(val1) or not is_integer(val2):
        raise LispError

    if key == "+":
        return val1 + val2
    if key == "-":
        return val1 - val2
    if key == "*":
        return val1 * val2
    if key == "/":
        return val1 // val2
    if key == "mod":
        return val1 % val2
    if key == ">":
        return val1 > val2


def evaluate(ast, env):
    if is_symbol(ast):
        return env.lookup(ast)

    if is_list(ast):
        if len(ast) > 2:
            key, *rest = ast
        else:
            key, rest = ast

        print(ast)
        print(key)
        print(rest)


        if key == "quote":
            return eval_quote(rest)

        if key == "atom":
            return eval_atom(rest,env)

        if key == "eq":
            return eval_eq(rest, env)

        if key in ["+", "-", "*", "/", "mod", ">"]:
            return eval_math(key, rest, env)

    return ast
