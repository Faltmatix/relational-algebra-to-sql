# The purpose of this file is to evaluate how
# well can the operators from operators.py
# run with a big amount of data
# Since we use python, we won't be as fast as
# possible but it is nice to evaluate how much
# time some operations can take


from operators import *
from utils import Database
from time import time

db = Database("../resources/big_data.db")

# The following data comes from kaggle :
# https://www.kaggle.com/szymonjanowski/internet-articles-data-with-users-engagement
articles = db.get_relation("articles_data")

def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time()
        function(*args, **kwargs)
        end_time = time()
        print(f"Finished {function.__name__} in {end_time-start_time:.4f} secs")
    return wrapper

@timer
def test1():
    request = Project(articles, "source_name")

@timer
def test2():
    request = Union(Project(articles, "author"), Project(articles, "author"))

@timer
def test3():
    request = Join(Project(articles, ["author", "description"]), Project(articles, ["author", "url"]))

@timer
def test4():
    request = Difference(articles, articles)


test1()
test2()
# Test 3 is a heavy operation, it might froze python for some seconds
# depending on the system specs
# test3()
