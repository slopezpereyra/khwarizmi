# khwarizmi

A simple library for efficiently solving basic algebraic expressions.

## Brief intro

This library works in a similar way an interpreter does. Its singularity is that what it interprets is a special kind of language: **algebra**.  

It allows you to work with equations, like this one,

    y = 2025.34x - 724

and get their solutions, their linear properties, attributes and more. For example, the solution of this equation when y
y equals 5 can be obtained. In just two lines <3 .
    
    >>>equation = SlopeIntercept('y = 2025.34x - 724')
    >>>equation.solve_for('y', 5)
    0.3599395657025487

Oh, it's like reading a poem... But how did I managed to do that?

Well, because algebraic properties can be represented as attributes of a thing far more consistently than as mere functional information, equations are treated as objects. Allowing you to treat your equations as instances of an algebraic class, this library essentially lets you cast, from a simple string, a rich mathematical object with its own unique properties and methods, and operate with it afterwards. 

It's efficient, it's easy and it's beautiful.

## What else can I do with it?

There are **tons of things** you can manage to easily pull off with khwarizmi. What khwarizmi does best is working with **linear equations**; refactoring, solving and graphing them can be easily done. Apart from linear equations, you can work with **standard and quadratic equations** and even **solve and graph systems of equations**.

On the Wiki you'll find reference pages from khwarizmi's modules. Refer ot its pages for more information, or dive into /docs/sample_code.md to see some examples of how khwarizmi actually looks like.

## Requirements

The only requirement for using the library are having **Python 3.x** and **matplotlib library** installed (the last is installed by default in most GNU/Linux distros so no problems there).

# Installation

To install the library for Python 3 use pip on your terminal.

    pip3 install khwarizmi --user

You are good to go now!
    


    

    
