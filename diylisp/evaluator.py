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
    print("env")
    print(env.bindings)

    if not is_list(ast):
        if is_boolean(ast):
            return ast
        elif is_integer(ast):
            return ast
        else:
            return env.lookup(ast)



    key, *rest = ast


    print(ast)
    print(key)
    print(rest)

    """Call to function should evaluate all arguments.

    When a function is applied, the arguments should be evaluated before being bound
    to the parameter names."""

    if is_closure(key):
        closure = key
        if len(closure.params) == 0:
            return evaluate(closure.body, closure.env)
        else:
            arguments = rest

            arg = []
            for argument in arguments:
                arg.append(evaluate(argument, env))




            if len(arg) == len(closure.params):
                new_env = {}
                for i in range(len(closure.params)):
                    new_env[closure.params[i]] = evaluate(arg[i],env)

                print(new_env)

                print("eval clos")

                return evaluate(closure.body, closure.env.extend(new_env))
            else:
                raise LispError("wrong number of arguments, expected %d got %d" % len(closure.params), len(arguments))



    if key == 'quote':
        if len(rest) == 1:
            return rest[0]
        else:
            raise LispError

    elif key == 'atom':
        rest = rest[0]
        if is_list(rest) and len(rest) > 1:
            res = evaluate(rest, env)
            print(res)
            return False if is_list(res) else True
        else:
            return True

    elif key == "lambda":
        if not len(rest) == 2:
            raise LispError("number of arguments")
        params, body = rest
        return Closure(env,params,body)

    if is_list(rest) and len(rest) == 2:
        value1, value2 = rest
    else:
        value1, value2 = rest, None


    if key == 'eq':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
        if is_list(value1) or is_list(value2):
            return False
        return value1 == value2

    elif key == "define":
        if value2:
            if isinstance(value1, str):
                return env.set(value1, evaluate(value2, env))
            else:
                raise LispError("non-symbol")
        else:
            raise LispError("Wrong number of arguments")


    if key == '+':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
        if is_integer(value1) and is_integer(value2):
            return value1 + value2
        else:
            raise LispError

    if key == '-':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
        if is_integer(value1) and is_integer(value2):
            return value1 - value2
        else:
            raise LispError

    if key == '/':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
        if is_integer(value1) and is_integer(value2):
            return value1 // value2
        else:
            raise LispError

    if key == '*':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
        if is_integer(value1) and is_integer(value2):
            return value1 * value2
        else:
            raise LispError

    if key == 'mod':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
        if is_integer(value1) and is_integer(value2):
            return value1 % value2
        else:
            raise LispError

    if key == '>':
        value1, value2 = evaluate(value1, env), evaluate(value2, env)
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


    res = evaluate(key, env)

    if not is_closure(res):
        raise LispError("not a function")


    return evaluate([res, rest],env)

