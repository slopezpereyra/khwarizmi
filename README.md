# khwarizmi-project
A library for solving quickly and efficiently algebraic expressions.

# How? 

This library works in a similar way an interpreter does. Its singularity is that what it interprets is a special kind of language: **algebra**. 

It works with classes because algebraic properties are more similar to attributes of a thing than to variables or mere information. To create an algebraic expression, you must only create an instance of the equation type that you wish (for example, a linear equation) and pass your equation (string) as an argument. For example:

    my_equation = Linear("y = 2x + 5")
    
Cool, uh?

# Cool things you can do with this library

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

