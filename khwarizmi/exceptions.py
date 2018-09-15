class _EquationError (Exception):
    """Baseclass for all equation-related errors."""

    def __init__(self):
        pass


class LinearSolutionError (_EquationError):

    def __init__(self):
        _EquationError.__init__(self)

    def __str__(self):
        error_string = ("You can not evaluate a linear equation without providing"
                        " an x or y value. Try solve_for () method instead.")

        return error_string
