# Sample code for Linear equations.

Given the object `equation = SlopeIntercept('y = 2x + 5')`

    >>>equation.form
    'Slope-Intercept Form
    >>>equation.x_mult
    '2'
    >>>equation.y_mult
    '1' 
    >>>equation.slope
    2
    >>>equation.y_intercept
    5
    >>> equation.get_point(2)
    (2, 9)
    >>> equation.points(2, 4)
    [(2, 9), (3, 11), (4, 13)]
    >>> points = equation.points(2, 4)
    >>> equation.graph(points)
![](https://github.com/lpereyrasantiago/khwarizmi/blob/master/resources/Figure_1.png)
    
    >>> equation.solve_for('x', 5)
    15
    >>> equation.solve_for('y', 2)
    -1.5
    >>> print(equation.express_as('Point-Slope'))
    y-9=2(x-2)
    >>> print(equation.express_as('Standard'))
    -2x+y=5
