
# Table of Contents

1.  [Getting started](#org46f6944)
2.  [The operators](#org085c97d)
    1.  [Select](#org239adc6)
    2.  [Project](#org38d537e)
    3.  [Join](#orgcf1c27a)
    4.  [Rename](#orgbb9962e)
    5.  [Union](#org8f3f5a5)
    6.  [Difference](#org0eb0d99)
3.  [Composed expressions](#org3c6bc2d)



<a id="org46f6944"></a>

# Getting started

In this section, I will walk you through how you can use the python
files to create SPJURD requests that works with an SQLite database.

First of all, you need to import the `operators.py` and `utils.py`
files. They are located in `./python/src/`. There are two ways to
play around with those files. You can either enter an interactive
python shell and test the commands from there or you can import
them into your script and work with them.

The `operators.py` file contains the SPJURD operators and relation
class. A relation is basically a 2D table with data types for
each column. You can instantiate your own relations but it is
easier to work directly with an SQLite database.

The `utils.py` file contains a way to seamlessly connect to an
SQLite database and work with the operators from there. You
can find some useful functions in there which are also used
in `operators.py`

You can find a database for testing purpose at
`./python/resources/testing.db`. If you modify these tables,
the unit tests might fail so it is recommanded to create your
own database for other purposes than testing.

Supposing you are in the ./python/src folder, the basic
workflow for using the files with a database is this :

    import os
    from operators import *
    from utils import Database
    
    # Specify the path to connect to your database
    # We currently are at ./python/src/ and we need the database from
    # ./python/resources/testing.db
    
    db = Database("../resources/testing.db")

Now that you have specified the location of your database,
you can get any table as an operator relation by giving the
name of the table as a string :

    cities = db.get_relation("cities")
    
    # For showing the table rows :
    print(cities.data)
    # For showing the columns data types :
    print(cities.dtypes)

You can of course use any operators on those relations.
The next section goes into details about them but here is
an example of Select :

    request = Select(cities, "Name", "Bergen")
    
    # The relation is stored in the result attribute of every operator
    print(request.result)


<a id="org085c97d"></a>

# The operators

Each operator is class that takes one or two relations with some other
parameters. The relation always comes first in the argument list.
When an operator is instantiated, it evaluates the operation
to do and stores the result inside itself. You can acces the
resulting relation with the .result attribute. Each operation
work as intended in the SPJRUD algebra. Below are examples
on how to use them.


<a id="org239adc6"></a>

## Select

    # Using a string to select
    request1 = Select(cities, "Country", "Belgium")
    # Using another data type
    request2 = Select(cities, "Population", 20.3)
    
    print(request1.result)
    # print(request1.sql)
    
    
    print(request2.result)
    # print(request2.sql)
    
    # Example using the column names
    select_r = db.get_relation("select_r")
    print(select_r)
    
    request3 = Select(select_r, "A", "C")
    print(request3.result)


<a id="org38d537e"></a>

## Project

    request = Project(cities, "Name")
    print(request.result)


<a id="orgcf1c27a"></a>

## Join

    r = db.get_relation("join_r")
    s = db.get_relation("join_s")
    
    print(r)
    print(s)
    
    request = Join(r, s)
    
    print(request.result)


<a id="orgbb9962e"></a>

## Rename

    request = Rename(cities, "Name", "cities")
    print(request.result)


<a id="org8f3f5a5"></a>

## Union

    union_r = db.get_relation("union_r")
    union_s = db.get_relation("union_s")
    request = Union(union_r, union_s)
    
    print(union_r)
    print(union_s)
    print(request.result)


<a id="org0eb0d99"></a>

## Difference

    request = Difference(union_r, union_s)
    print(request.result)


<a id="org3c6bc2d"></a>

# Composed expressions

In this section, I give some examples on how to combine the expressions
together

Select the name of the city with 20.3 in population

    request = Project(Select(cities, "Population", 20.3), "Name")
    print(request.result)

    request = Union(Select(cities, "Name", "Brussels"), Select(cities, "Population", 20.3))
    print(request.result)

    countries = db.get_relation("countries")
    capitals = Rename(Project(countries, ["Capital", "Name", "Population"]), "Name", "Country")
    all_cities = Union(Rename(capitals, "Capital", "Name"), cities)
    print(all_cities.result)

