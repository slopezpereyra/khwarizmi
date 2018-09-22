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
