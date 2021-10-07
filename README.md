# khwarizmi

A library for efficiently solving algebraic operations.

### Presentation

This library works in a similar way an interpreter does. Its singularity is that what it interprets is a special kind of language: **algebra**.  

The interpretation of algebraic expressions is made through a process of partition, in which simple string representations of algebraic expressions are divided into smaller algebraic components, the most basic of which are terms. The expressions are enriched with a meaningful set of attributes that allow the extension of some basic properties to more complex ones. As in mathematics, the most complex parts of Khwarizmi are built upon just a few foundational operations. 

Despite the richness of the mathematical objects created by Khwarizmi, the algorithms are incredibly unexpensive, and they all eventually come down to the cheap interpretation of a string.

### Current features

Khwarizmi began as an equation solver. Today, apart from solving and graphing equations of degree n = 1 and n = 2, it allows a full interpretation of linear equations, the construction of meaningful polynomials, operations between algebraic terms, and solving and graphing systems of equations.

### Requirements

The only requirement for using the library are having **Python 3.x** and **matplotlib library** installed (the last is installed by default in most GNU/Linux distros).

## Installation

To install the library for Python 3 use pip on your terminal.

    pip3 install khwarizmi --user


    


    

    
