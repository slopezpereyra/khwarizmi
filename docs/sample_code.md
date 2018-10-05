# Sample code for Linear equations.

This code was sampled using Python 3.6 IDLE after declaring

    from khwarizmi import linear

Given the object `equation = SlopeIntercept('y = 2x + 5')`

    >>>equation.form
    'Slope-Intercept Form'
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

# Sample code for Systems of equations

This code was sampled using Python 3.6 IDLE after declaring

    from khwarizmi import linear

Given the following system

    >>> first_equation = linear.SlopeIntercept('y = 2x + 5')
    >>> second_equation = linear.Standard ('3x + 2y = 8')
    >>> system = linear.LinearSystem(first_equation, second_equation)
    
We can state:
    
    >>> system.solutions
    'One solution'
    >>> system.compatible
    True
    >>> system.solve()
    (-0.2857142857142857, 4.428571428571429)
    >>> system.graph()
![](https://github.com/lpereyrasantiago/khwarizmi/blob/master/resources/system%20of%20equations.png)


    
