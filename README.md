# khwarizmi

A simple library for quickly and efficiently solving basic algebraic expressions.

# Quick intro

This library works in a similar way an interpreter does. Its singularity is that what it interprets is a special kind of language: **algebra**. It works with classes because algebraic properties are more similar to attributes of a thing than to variables or mere information. 

# How?

## Creating equations

To create an algebraic expression, you must only create an instance of the equation type that you wish (for example, a linear equation) and pass your equation (string) as an argument. For example:

    my_equation = Linear("y = 2x + 5")
 
 Current equations types supported are:
 
 * Equation : regular equation with a single variable, such as **2x+5 = 9**
 * Linear : a linear equation of any form.
 * SlopeIntercept : a linear equation under the Slope-Intercept form.
 * PointSlope : a linear equation under the Point-Slope form.
 * Standard : a linear equation under the Standard Form.
 * Quadratic : an equation of quadratic form (currently only supports those that are equal to 0).
 
 It is best to use specific forms of equations when working with linear equations and avoid using the **Linear** general class for the sake of specificity. This way,
 
     SlopeIntercept("y = 2x + 5") 
 
 is prefered over
 
    Linear("y = 2x + 5")
    
though both will work just fine.

# Useful methods

## 'Regular' equations

After the instantiation of an equation of type **Equation**, we can access many attributes that will be defined on intialization. Provided the equation:

    my_equation = Equation("234x - 45 = 33.6")
    
We can say:

    # Attributes

    >>>print(my_equation.inc_side) # side of the equation the incognito is in.
    234x-5
    >>>print(my_equation.sol_side) # side of equation the solution to the incognito is in.
    33.6
    >>>print(my_equation.incognito) # the incognito of this equation
    x
    >>>print(my_equation.incognito_index) # position of the incognito on the equation
    3
    >>>print(my_equation.inc_multiplier) # the incognito multiplier; i.e. the number that multiplies the incognito.
    234
    >>> print(my_equation.inc_mult_index) # index of the incognito multiplier. If it has more than one digit, index of the first.
    0

    # Methods
    
    >>>print(my_equation.sort_equation()) # This method returns as a string the equation sorted and ready to be solved.
    x = (33.6+45)/234
    >>>print(my_equation.solve()) # Returns the solution of the equation; in this case, the value of x.
    0.335897435897

## Linear equations

Linear equations are currently the more richly supported. Let's see class by class what we can do.

    a = SlopeIntercept("y = 5x - 3")
    b = PointSlope("y - 9 = 5 (x + 3)")
    c = Standard("2x + 5y = 9")

Now lets work some magic with them. For example, lets see what is the form of this linear equations.

    # Attributes
    
    >>>print("FORM OF A: ", a.form)
    FORM OF A: Slope-Intercept Form
    >>>print("FORM OF B: ", b.form)
    FORM OF B: Point-Slope Form
    >>>print("FORM OF C: ", c.form
    FORM OF C: Standard Form
    
    # Methods
    
    >>>print(a.get_point(5)) # the point (tuple) formed by equation a when x = 5.
    (5, 22)
    >>>print(b.get_point(2349)) # the point (tuple) formed by equation b when x = 2349.
    (2349, 11760)
    >>> print(c.get_point(2)) # the point (tuple) formed by equation c when x = 2.
    (2, 1.0)

    >>>print(a.points(1, 3)) # Returns a list of all points formed for every value of x from 1 to 3 (inclusive).
    [(1, 2), (2, 7), (3, 12)]
    >>>print(b.points(2498, 2503)) # Return a list of all points formed for every value of x from 2498 to 2503 (inclusive).
    [(2498, 12487), (2499, 12492), (2500, 12497), (2501, 12502), (2502, 12507), (2503, 12512)]
    
Now let's solve our equations. Since linear equations have two incognitos, we can not solve them without providing a specific value for x or y. To do this, we use the **solve_for()** method.

    >>>print(a.solve_for("x", 3)) # Solve the equation a when x = 3.
    12
    >>>print(b.solve_for("y", 1.03486)) # Solve the equation b when y = 1.03486.
    1.4069720000000001
    >>>print(c.solve_for("x", 5)) # Solve the equation c when x = 5.
    -0.2
    
    # We could set the optional **show** argument to True in order to see the operation happen,

    >>>print(a.solve_for("x", 3, True)) # Solve the equation a when x = 3 and show operation
     y=5*3-3
    12
    
    >>>print(b.solve_for("y", 1.03486, True)) # Solve the equation b when y = 1.03486 and show operation.
    x=(1.03486-9+5*3)/5
    1.4069720000000001
    
    # You get the picture.
    
Let's take a look at a very important linear method: the **express_as(form)** method.

    # express_as(form) returns an instance of the equation under the form it is passed as an argument.
    
    # Re-expressing equation a:
    
    >>>print(a.express_as("Standard")) # returns an instance of the Standard class with an equation equivalent to a.
    -5.0x+y=-3.0 
    
    # Notice that -5x+y = -3 is just the equation a 'y = 5x + 3' written in Standard form.
    
    # since this returns an instance of the Standard class, we can save it into a variable.
    
    standard_a = a.express_as("Standard"))
    
    # This is equivalent to saying
    
    a_standard = Standard('-5x+y=-3')

    # Let's convert it to Point-Slope form now.
    
    >>>a_point_slope = a.express_as("Point-Slope")
    >>>print(a_point_slope)
    y-7.0=5.0(x-2)

Of course, you can re-express in different forms any equation. Statements such as

    b.express_as("Slope-Intercept")
    c.express_as("Point-Slope")
    
are valid too, and will perform the same operations shown above.

## Quadratic equations

Currently, only quadratic equations that are equal to 0 are supported.

Let's say
   
    QUA = Quadratic("5x**2 + 6x**2 + 1 = 0")
    
Then, 

    >>>print(QUA.formulate()) # Returns a string of the equation written to be solved on the quadratic formula.
    (-6±√6̅*̅*̅2̅-̅4̅*̅5̅*̅1̅)/2*5
    >>>print(QUA.plus_solution) # solution for -b + square root of b squared minus 4 times a times c over 2 times a.
    -0.2
    >>>print(QUA.minus_solution) # solution for -b - square root of b squared minus 4 times a times c over 2 times a.
    -1.0
    
    


    

    
