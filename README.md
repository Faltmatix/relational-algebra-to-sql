#+TITLE: Readme

* Getting started

In this section, I will walk you through how you can use the python
files to create SPJURD requests that works with an SQLite database.

First of all, you need to import the =operators.py= and =utils.py=
files. They are located in =./python/src/=. There are two ways to
play around with those files. You can either enter an interactive
python shell and test the commands from there or you can import
them into your script and work with them.

The =operators.py= file contains the SPJURD operators and relation
class. A relation is basically a 2D table with data types for
each column. You can instantiate your own relations but it is
easier to work directly with an SQLite database.

The =utils.py= file contains a way to seamlessly connect to an
SQLite database and work with the operators from there. You
can find some useful functions in there which are also used
in =operators.py=

You can find a database for testing purpose at
=./python/resources/testing.db=. If you modify these tables,
the unit tests might fail so it is recommanded to create your
own database for other purposes than testing.

Supposing you are in the ./python/src folder, the basic
workflow for using the files with a database is this :

#+BEGIN_SRC python :session readme :results output :exports both
import os
from operators import *
from utils import Database

# Specify the path to connect to your database
# We currently are at ./python/src/ and we need the database from
# ./python/resources/testing.db

db = Database("../resources/testing.db")
#+END_SRC

Now that you have specified the location of your database,
you can get any table as an operator relation by giving the
name of the table as a string :

#+BEGIN_SRC python :session readme :results output :exports both
cities = db.get_relation("cities")

# For showing the table rows :
print(cities.data)
# For showing the columns data types :
print(cities.dtypes)

#+END_SRC

#+RESULTS:
: [('Bergen', 'Belgium', 20.3), ('Bergen', 'Norway', 30.5), ('Brussels', 'Belgium', 370.6)]
: {'Name': 'text', 'Country': 'text', 'Population': 'real'}

You can of course use any operators on those relations.
The next section goes into details about them but here is
an example of Select :

#+BEGIN_SRC python :session readme :results output :exports both
request = Select(cities, "Name", "Bergen")

# The relation is stored in the result attribute of every operator
print(request.result)
#+END_SRC

#+RESULTS:
: cities
: {'Name': 'text', 'Country': 'text', 'Population': 'real'}
: ('Bergen', 'Belgium', 20.3)
: ('Bergen', 'Norway', 30.5)


* The operators

Each operator is class that takes one or two relations with some other
parameters. The relation always comes first in the argument list.
When an operator is instantiated, it evaluates the operation
to do and stores the result inside itself. You can acces the
resulting relation with the .result attribute. Each operation
work as intended in the SPJRUD algebra. Below are examples
on how to use them.

** Select

#+BEGIN_SRC python :session readme :results output :exports both
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
#+END_SRC

#+RESULTS:
#+begin_example
cities
{'Name': 'text', 'Country': 'text', 'Population': 'real'}
('Bergen', 'Belgium', 20.3)
('Brussels', 'Belgium', 370.6)

cities
{'Name': 'text', 'Country': 'text', 'Population': 'real'}
('Bergen', 'Belgium', 20.3)

select_r
{'A': 'integer', 'B': 'integer', 'C': 'integer'}
(1, 3, 2)
(1, 4, 1)
(2, 4, 2)
(2, 3, 1)

select_r
{'A': 'integer', 'B': 'integer', 'C': 'integer'}
(1, 4, 1)
(2, 4, 2)
#+end_example


** Project

#+BEGIN_SRC python :session readme :results output :exports both
request = Project(cities, "Name")
print(request.result)
#+END_SRC

#+RESULTS:
: cities
: {'Name': 'text'}
: ['Bergen']
: ['Bergen']
: ['Brussels']

** Join

#+BEGIN_SRC python :session readme :results output :exports both
r = db.get_relation("join_r")
s = db.get_relation("join_s")

print(r)
print(s)

request = Join(r, s)

print(request.result)
#+END_SRC

#+RESULTS:
#+begin_example
join_r
{'A': 'integer', 'B': 'integer', 'C': 'integer'}
(1, 3, 5)
(1, 4, 5)
(2, 4, 5)
(2, 3, 6)

join_s
{'B': 'integer', 'C': 'integer', 'D': 'integer'}
(3, 5, 2)
(4, 5, 2)
(4, 5, 1)
(4, 6, 1)

join_r
{'A': 'integer', 'B': 'integer', 'C': 'integer', 'D': 'integer'}
[1, 3, 5, 2]
[1, 4, 5, 2]
[1, 4, 5, 1]
[2, 4, 5, 2]
[2, 4, 5, 1]
#+end_example

** Rename

#+BEGIN_SRC python :session readme :results output :exports both
request = Rename(cities, "Name", "cities")
print(request.result)
#+END_SRC

#+RESULTS:
: cities
: {'cities': 'text', 'Country': 'text', 'Population': 'real'}
: ('Bergen', 'Belgium', 20.3)
: ('Bergen', 'Norway', 30.5)
: ('Brussels', 'Belgium', 370.6)

** Union

#+BEGIN_SRC python :session readme :results output :exports both
union_r = db.get_relation("union_r")
union_s = db.get_relation("union_s")
request = Union(union_r, union_s)

print(union_r)
print(union_s)
print(request.result)
#+END_SRC

#+RESULTS:
#+begin_example
union_r
{'A': 'integer', 'B': 'integer', 'C': 'integer'}
(1, 3, 5)
(1, 4, 5)

union_s
{'A': 'integer', 'B': 'integer', 'C': 'integer'}
(1, 4, 5)
(2, 3, 6)

union_r
{'A': 'integer', 'B': 'integer', 'C': 'integer'}
(1, 3, 5)
(1, 4, 5)
(2, 3, 6)
#+end_example

** Difference

#+BEGIN_SRC python :session readme :results output :exports both
request = Difference(union_r, union_s)
print(request.result)
#+END_SRC

#+RESULTS:
: union_r
: {'A': 'integer', 'B': 'integer', 'C': 'integer'}
: (1, 3, 5)

* Composed expressions

In this section, I give some examples on how to combine the expressions
together

Select the name of the city with 20.3 in population
#+BEGIN_SRC python :session readme :results output :exports both
request = Project(Select(cities, "Population", 20.3), "Name")
print(request.result)
#+END_SRC

#+RESULTS:
: cities
: {'Name': 'text'}
: ['Bergen']


#+BEGIN_SRC python :session readme :results output :exports both
request = Union(Select(cities, "Name", "Brussels"), Select(cities, "Population", 20.3))
print(request.result)
#+END_SRC

#+RESULTS:
: cities
: {'Name': 'text', 'Country': 'text', 'Population': 'real'}
: ('Brussels', 'Belgium', 370.6)
: ('Bergen', 'Belgium', 20.3)

#+BEGIN_SRC python :session readme :results output :exports both
countries = db.get_relation("countries")
capitals = Rename(Project(countries, ["Capital", "Name", "Population"]), "Name", "Country")
all_cities = Union(Rename(capitals, "Capital", "Name"), cities)
print(all_cities.result)
#+END_SRC

#+RESULTS:
: countries
: {'Name': 'text', 'Country': 'text', 'Population': 'real'}
: ['Brussels', 'Belgium', 10255.6]
: ['Oslo', 'Norway', 4463.2]
: ['Tokyo', 'Japan', 128888.0]
: ('Bergen', 'Belgium', 20.3)
: ('Bergen', 'Norway', 30.5)
: ('Brussels', 'Belgium', 370.6)
