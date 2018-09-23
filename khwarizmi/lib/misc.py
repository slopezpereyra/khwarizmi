"""Useful and simple math methods."""


def num(a):
    """Returns a number representation of string a as a float
    if a represents a float; otherwise, as an int.

    Keyword arguments:

    a : string representation of a float or int."""

    try:
        return int(a)
    except ValueError:
        return float(a)


def cond_assign(condition, if_true, if_false):
    """Method for conditional assignments.
    If condition is true returns if_true,
else returns if_false. Saves lines and ugly if-else use."""

    return if_true if condition else if_false
