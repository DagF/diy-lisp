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
    return rest[0]

def eval_atom(rest,env):
    return is_atom(evaluate(rest[0],env))

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

def eval_if(rest,env):
    expres, res1, res2 = rest
    if evaluate(expres, env):
        return evaluate(res1, env)
    else:
        return evaluate(res2, env)


def eval_define(rest, env):
    try:
        symbol, value = rest
    except:
        raise LispError("Wrong number of arguments")


    if not is_symbol(symbol):
        raise LispError("non-symbol")

    return env.set(symbol, evaluate(value, env))


def eval_lambda(rest, env):
    try:
        params, body = rest
    except:
        raise LispError("number of arguments")

    return Closure(env, params, body)

def eval_closure(closure,params, env):
    new_env = {}
    for i in range(len(closure.params)):
        new_env[closure.params[i]] = evaluate(params[i], env)

    if is_list(params) and len(params) != len(closure.params):
        raise LispError("wrong number of arguments, expected %d got %d" % (len(closure.params), len(params)))
    return evaluate(closure.body, closure.env.extend(new_env))

def eval_cons(rest, env):
    head = [evaluate(rest[0], env)]
    tail = evaluate(rest[1], env)

    if not is_list(tail):
        tail = [tail]
    return head + tail

def eval_head(rest, env):
    try:
        return evaluate(rest[0], env)[0]
    except:
        raise LispError

def eval_tail(rest, env):
    list = rest[0]

    list = evaluate(list, env)

    if not is_list(list):
        raise LispError

    if len(list) == 0:
        raise LispError

    return list[1:]


def eval_empty(rest, env):
    list = rest[0]

    list = evaluate(list, env)

    if not is_list(list):
        raise LispError

    return len(list) == 0


def evaluate(ast, env):
    print("ast")
    print(ast)
    print("env")
    print(env.bindings)

    if is_symbol(ast):
        return env.lookup(ast)

    if is_list(ast):
        if len(ast) >= 2:
            key = ast[0]
            rest = ast[1:]
        elif len(ast) == 1:
            key = ast[0]
            rest = None
        else:
            raise LispError


        print("Key")
        print(key)
        print("rest")
        print(rest)

        if is_list(key):
            key = evaluate(key, env)

        if is_closure(key):
            return eval_closure(key, rest, env)

        if key == "quote":
            return eval_quote(rest)

        if key == "atom":
            return eval_atom(rest,env)

        if key == "eq":
            return eval_eq(rest, env)

        if key in ["+", "-", "*", "/", "mod", ">"]:
            return eval_math(key, rest, env)

        if key == "if":
            return eval_if(rest, env)

        if key == "define":
            return eval_define(rest, env)

        if key == "lambda":
            return eval_lambda(rest, env)

        if key == "cons":
            return eval_cons(rest, env)

        if key == "head":
            return eval_head(rest, env)

        if key == "tail":
            return eval_tail(rest, env)

        if key == "empty":
            return eval_empty(rest, env)


        if is_symbol(key):
            key = evaluate(key, env)

            if is_closure(key):
                return eval_closure(key, rest, env)

        raise LispError("not a function")



    if is_closure(ast):
        return eval_closure(ast, rest, env)

    return ast
