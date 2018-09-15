# khwarizmi-project
A library for solving quickly and efficiently algebraic expressions.

# How? 

This library works in a similar way an interpreter does. Its singularity is that what it interprets is a special kind of language: **algebra**. 

It works with classes because algebraic properties are more similar to attributes of a thing than to variables or mere information. To create an algebraic expression, you must only create an instance of the equation type that you wish (for example, a linear equation) and pass your equation (string) as an argument. For example:

    my_equation = Linear("y = 2x + 5")
    
Cool, uh?

# Cool things you can do with this library

## Standard equations

Let's see some simple things you can do with the standard type of equation. This is any equation that is not linear or cuadratic. For example,

    my_equation = Equation("234x - 45 = 33.6")
    
Let's say we only want to access one side of the equation; for example, the one the incognito (x) is in.

    print(my_equation.inc_side) # side of the incognito
    print(my_equation.sol_side) # side of the solution
    
This would print

    234x-5
    33.6
    
with the spaces removed for convenience.

Let's do some more interesting things now.

    print(my_equation.sort_equation())
    
This would print your equation sorted with the incognito cleared and all the proper operations on the solution side. Like this:

    x = (33.6+45)/234
    
Finally, let's see what the result of this equation is.

    print(my_equation.solve())
   
This would return the value of x:

    0.335897435897
    
Cool!

## Linear equations

There's a whole set of functions and attributes you can use and access for linear equations. Let's see some of them using the following two linear equations:

    a = Linear("y = 5x - 3")
    b = Linear("y - 9 = 5 (x + 3)")
    
Now lets work some magic with them. For example, lets see what is the form of this linear equations. The statement

    print("FORM OF A: ", a.form)
    print("FORM OF B: ", b.form)

would print 
    
    FORM OF A: Slope-Intercept Form
    FORM OF B: Point-Slope Form
    
 Lets see now how we could get one and many points formed by given x values on this equations.
 
    print(a.get_point(5)) # the point formed by equation a when x = 5.
    print(b.get_point(2349)) # the point formed by equation b when x = 2349
    
This will return
    
    (5, 22) # tuple of x-y values.
    (2349, 11760) # tuple of x-y values.
    
Lets say I want to know the set of points formed by an equation for multiple values of x. This can be done with the following statement.

    print(a.points(1, 3)) # Return a list of all points formed for every value of x from 1 to 3 (inclusive).
    print(b.points(2498, 2503)) # Return a list of all points formed for every value of x from 2498 to 2503 (inclusive).
    
This would print

    [(1, 2), (2, 7), (3, 12)]
    [(2498, 12487), (2499, 12492), (2500, 12497), (2501, 12502), (2502, 12507), (2503, 12512)]
    

Now let's solve our equations. Since linear equations have two incognitos, we can not solve them without providing a specific value for x or y. To do this, we use the **solve_for()** method.

    print(a.solve_for("x", 3)) # Solve the equation a when x = 3.
    print(b.solve_for("y", 1.03486)) # Solve the equation b when y = 1.03486.
    
This would return

    12
    1.4069720000000001

We could set the optional **show** argument to __True__ in order to see the operation happen,

    print(a.solve_for("x", 3, True)) # Solve the equation a when x = 3 and show operation
    print("") # leave a space...
    print(b.solve_for("y", 1.03486, True)) # Solve the equation b when y = 1.03486 and show operation.
    
which would return

    y=5*3-3
    12
    
    x=(1.03486-9+5*3)/5
    1.4069720000000001
    
Cool :)

    


    

    
