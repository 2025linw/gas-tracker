from functools import wraps
from uuid import UUID

from flask import session

from const import NOT_AUTHENTICATED


"""
Type Checker
"""
def is_uuid(uuid_str: str) -> bool:
    try:
        UUID(uuid_str)

        return True
    except ValueError:
        return False


"""
Decorators
"""
def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return NOT_AUTHENTICATED, 401

        return f(*args, **kwargs)

    return wrapper


"""
Formatting Helpers
"""
def snake_to_camelCase(string):
    """
    Converts a snake_case string into a camelCase string

    Args:
        string (str): string in snake_case
    """

    tokens = string.split("_")
    out = tokens[0]
    for tok in tokens[1:]:
        out += tok.capitalize()

    return out

def dict_snake_to_camelCase(dictionary):
    """
    Converts all keys of a Python dict from snake_case to camelCase

    Args:
        dict (dict): Python dictionary with keys in snake_case

    Returns:
        dict: input dictionary with keys in camelCase
    """

    ret = {}
    for val in dictionary:
        ret[snake_to_camelCase(val)] = dictionary.get(val)

    return ret
