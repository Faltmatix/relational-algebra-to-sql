import unittest
from operators import *
import utils

db = utils.Database("../resources/testing.db")

#class TestQuery(unittest.TestCase):

class TestSelect(unittest.TestCase):

    def test_atomic1(self):

        r = db.get_relation("select_r")
        select = Select(r, "A", 1)

        # Expected results
        dtypes = r.dtypes
        data = [(1, 3, 2),
                (1, 4, 1)]
        rel = Rel(dtypes, data)

        self.assertTrue(select.result == rel)

    def test_atomic2(self):

        r = db.get_relation("select_r")
        select = Select(r, "A", "C")

        # Expected results
        dtypes = r.dtypes
        data = [(1, 4, 1),
                (2, 4, 2)]

        rel = Rel(dtypes, data)

        print(rel, select.result)

        self.assertTrue(select.result == rel)


class TestProject(unittest.TestCase):
    """"""

    r = db.get_relation("students")

    # Object to evaluate
    proj1 = Project(["id", "name"], r)
    proj2 = Project(["name", "id"], r)

    # Expected results
    eres1 = Rel({"id":"integer", "name":"text"},
                [[1, "Adrien"], [2, "Loic"]],
                name="students")
    eres2 = Rel({"name":"text", "id":"integer"},
                [["Adrien", 1], ["Loic", 2]],
                name="students")

    def test_atomic1(self):
        self.assertTrue(TestProject.eres1 == TestProject.proj1.result)

    def test_atomic2(self):
        self.assertTrue(TestProject.eres2 == TestProject.proj2.result)

class TestJoin(unittest.TestCase):

    def test_atomic(self):

        r = db.get_relation("join_r")
        s = db.get_relation("join_s")
        join = Join(r,s)

        # Expected result
        dtypes = {'A': 'integer',
                  'B': 'integer',
                  'C': 'integer',
                  'D': 'integer'}

        # TODO : unifier data en tuple
        data = [[1, 3, 5, 2],
                [1, 4, 5, 2],
                [1, 4, 5, 1],
                [2, 4, 5, 2],
                [2, 4, 5, 1]]

        rel = Rel(dtypes, data)

        self.assertTrue(join.result == rel)




class TestRename(unittest.TestCase):

    def test_atomic(self):

        r = db.get_relation("students")
        rename = Rename(r, "age", "Age")

        # Expected result
        dtypes = {'id': 'integer',
                  'name': 'text',
                  'Age': 'int',
                  'studies': 'text'}

        data = [(1, 'Adrien', 20, 'Computer Science'),
                (2, 'Loic', 20, 'Engineering')]

        rel = Rel(dtypes, data)

        self.assertTrue(rename.result == rel)

class TestUnion(unittest.TestCase):

    def test_atomic(self):

        r = db.get_relation("union_r")
        s = db.get_relation("union_s")
        union = Union(r, s)

        # Expected result
        dtypes = r.dtypes
        data = [(1, 3, 5),
                (1, 4, 5),
                (2, 3, 6)]

        rel = Rel(dtypes, data)

        self.assertTrue(union.result == rel)


class TestDifference(unittest.TestCase):

    def test_atomic(self):

        r = db.get_relation("union_r")
        s = db.get_relation("union_s")
        difference = Difference(r, s)

        # Expected result
        dtypes = r.dtypes
        data = [(1, 3, 5)]
        rel = Rel(dtypes, data)

        self.assertTrue(difference.result == rel)

#class ComposedRequests(unittest.TestCase):

if __name__ == "__main__":

    unittest.main()
