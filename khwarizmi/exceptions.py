class _EquationError (Exception):
    """Baseclass for all equation-related errors."""

    def __init__(self):
        pass


class NoVariableError (_EquationError):

    def __init__(self, equation):
        _EquationError.__init__(self)
        self.equation = equation

    def __str__(self):
        error_string = "There's no variable nor incognito to be cleared on the equation " + self.equation

        return error_string


class NoEqualityError (_EquationError):

    def __init__(self, equation):
        _EquationError.__init__(self)
        self.equation = equation

    def __str__(self):
        error_string = "The equation " + self.equation + " doesn't express an equality."

        return error_string


class LinearSolutionError (_EquationError):

    def __init__(self):
        _EquationError.__init__(self)

    def __str__(self):
        error_string = ("You can not evaluate a linear equation without providing"
                        " an x or y value. Try solve_for () method instead.")

        return error_string


class NegativeSquareError(_EquationError):

    def __init__(self):
        _EquationError.__init__(self)

    def __str__(self):
        error_string = ("This quadratic equation has a negative square"
                        " and can't be solved.")

        return error_string
