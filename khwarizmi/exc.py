"""Defines exceptions for this package."""


class _AlgebraicError (Exception):
	"""Base class for all equation-related errors."""

	def __init__(self):
		pass


class UnableToDefineFormError(_AlgebraicError):

	def __init__(self, equation):
		_AlgebraicError.__init__(self)
		self.equation = equation

	def __str__(self):

		error_string = """Khwarizmi was unable to define a form for {}.
		Your linear equation should be on Standard,                 
		Slope-Intercept or Point-Slope form.""".format(self.equation)

		return error_string


class NoVariableError (_AlgebraicError):

	def __init__(self, equation):
		_AlgebraicError.__init__(self)
		self.equation = equation

	def __str__(self):
		error_string = "There's no variable nor incognito to be cleared on the equation " + self.equation

		return error_string


class NoEqualityError (_AlgebraicError):

	def __init__(self, equation):
		_AlgebraicError.__init__(self)
		self.equation = equation

	def __str__(self):
		error_string = "The equation " + self.equation + " doesn't express an equality."

		return error_string


class LinearSolutionError (_AlgebraicError):

	def __init__(self):
		_AlgebraicError.__init__(self)

	def __str__(self):
		error_string = ("You can not evaluate a linear equation without providing"
						" an x or y value. Try solve_for () method instead.")

		return error_string


class UnsuitableSlopeInterceptForm(_AlgebraicError):

	def __init__(self, equation):
		_AlgebraicError.__init__(self)
		self.equation = equation

	def __str__(self):
		error_string = """This Slope-Intercept equation {} is unsuitable, probably                        
						because y is multiplied by some value n or you are multiplying 
						the whole solution side by some value m. If your equation looks like
						y = m (x + i) or ny = x + i, write the equation with the value m or n
						distributed to form a pure Slope-Intercept equation.""".format(self.equation)
		return error_string


class NegativeSquareError(_AlgebraicError):

	def __init__(self):
		_AlgebraicError.__init__(self)

	def __str__(self):
		error_string = """"This quadratic equation has a negative square
						and can't be solved."""

		return error_string


class ConversionError(_AlgebraicError):

	def __init__(self):
		_AlgebraicError.__init__(self)
		pass


class InvalidFormError(ConversionError):

    def __init__(self, form):
        super().__init__()

    def __str__(self):

        error_string = """The form passed as a convertion argument is not valid. Valid
        forms are LinearForms.PointSlope, LinearForms.Standard, LinearForms.SlopeIntercept."""


class RedundantConversionError(ConversionError):

    def __init__(self, form, intended):
        super().__init__()
        self.form = form
        self.intended = intended

    def __str__(self):
        error_string = "Converting {} equation into {} Form is redundant.".format(
            self.form, self.intended)

        return error_string


class InfinitelySolutionsError(_AlgebraicError):

    def __init__(self):
        super().__init__()

    def __str__(self):
        error_string = """You are requesting a solution for a system of equations
        and there's an infinite number of them."""

        return error_string


class InvalidOperationError(_AlgebraicError):

    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def __str__(self):
        error_string = """Failed to perform operation between {} and {}.
        It is likely that {} and/or {} are not of the type
        required by the operation.""".format(self.a, self.b, self.a, self.b)

        return error_string


class NonAlgebraicOperationError(_AlgebraicError):

    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def __str__(self):

        error_string = """The operation between {} and {} was unsuccessful.
        It either can't be done (only one of the expressions is algebraic)
        or should be done with built-in operations 
        (if neither of the expressions is algebraic).""".format(self.a, self.b)

        return error_string
