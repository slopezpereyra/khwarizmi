"""Useful and simple math methods."""


def num(value):
    """Returns a float or an int representation of value
    after defining which should be the case.

    Keyword arguments:

    a : string representation of a value or numerical value."""

    return int(value) if str(value).endswith(".0") else float(value)


def cond_assign(condition, if_true, if_false):
    """Method for conditional assignments.
    If condition is true returns if_true,
else returns if_false. Saves lines and ugly if-else use."""

    return if_true if condition else if_false
