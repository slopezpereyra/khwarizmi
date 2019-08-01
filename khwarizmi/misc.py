"""Useful and simple miscellaneous methods."""

IGNORED = ['/', '*']


def num(value):
    """Returns a float or an int representation of value
    after defining which should be the case.

    Keyword arguments:

    a : string representation of a value or numerical value."""

    # Profilactic measure. Also keeps things neater on other algorithms.
    value = str(value)

    if isafraction(value):
        value = frac_to_num(value)

    if '.' in str(value) and not str(value).endswith('.0'):
        return float(value)
    elif '.' in str(value) and str(value).endswith('.0'):
        return int(value[:-2])
    # This elif is sloppy and buggy. Fix it right away.
    elif '*' in str(value):
        return eval(value)
    else:
        return int(value)


def isafraction(string):

    if not type(string) is str:
        return False
    return isanumber(string) and '/' in string


def are_operable(a, b):
    """Returns true if the addition or substraction
    between terms a and b can be done with simplification."""

    return (isanumber(a) and isanumber(b)) or (not isanumber(a) and not isanumber(b))


def isanumber(string):
    """Returns true if the string is representing a number"""

    has_digits = False

    if string.isdigit():
        return True

    if string.startswith('-') and string [1:].isdigit():
        return True

    index = 0
    for char in string:
        if char.isdigit() and has_digits is False:
            has_digits = True

        if index is 0 and string[index] is '-':
            index += 1
            continue

        if not char.isdigit() and not char in IGNORED:
            return False

        index += 1

    return has_digits


def frac_to_num(frac):

    if frac.isalpha() or frac == '':
        return frac
    return str(eval(frac))


def if_assign(condition, if_true, if_false):
    """Method for conditional assignments.
    If condition is true returns if_true,
    else returns if_false. Saves lines and ugly if-else use."""

    return if_true if condition else if_false


