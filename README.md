# khwarizmi

A simple library for efficiently solving basic algebraic expressions.

## Brief intro

Did you ever think you'd be able to have this linear equation,

    y = 2025.34x - 724

and get its solution when y equals 5 on Python with a single function? Now you can. In just two lines.
    
    >>>equation = SlopeIntercept('y = 2025.34x - 724')
    >>>equation.solve_for('y', 5)
    0.3599395657025487

Oh, it's like reading a poem... But how did I managed to do that?

Well, this library works in a similar way an interpreter does. Its singularity is that what it interprets is a special kind of language: **algebra**. 

Because algebraic properties can be represented as attributes of a thing far more consistently than as mere functional information, equations are treated as objects. Allowing you to treat your equations as instances of an algebraic class, it essentially lets you cast, from a simple string, a rich mathematical object with its own unique properties and methods, and operate with it afterwards. 

Did I mention it all feels as beautiful as a fricking poem?

## Requirements

The only requirement for using the library are having **Python 3.x** and **matplotlib library** installed (the last is installed by default in most GNU/Linux distros so no problems there).

# Installation

To install the library for Python 3 use pip on your terminal.

    pip3 install khwarizmi --user

You are good to go now!

## What can I do with it?

There are **tons of things** you can manage to easily pull off with khwarizmi. What khwarizmi does best is working with **linear equations**, but you can also solve **standard and quadratic equations** with it. **You can even solve systems of equations with it!**

On the Wiki you'll find examples and basic instructions that will show you how khwarizmi works more interactively. Refer ot its pages for more information!
    


    

    
