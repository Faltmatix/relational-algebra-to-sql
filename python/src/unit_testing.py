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

        self.assertTrue(select.result == rel)

class TestProject(unittest.TestCase):
    """"""

    r = db.get_relation("students")

    # Object to evaluate
    proj1 = Project(r, ["id", "name"])
    proj2 = Project(r, ["name", "id"])

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

class ComposedRequests(unittest.TestCase):

    def test_project_select(self):

        r = db.get_relation("students")
        request = Project(Select(r, "age", 20), "name")

        # Expected result
        dtypes = {"name":"text"}
        data = [['Adrien'], ['Loic']]
        rel = Rel(dtypes, data)

        self.assertTrue(request.result == rel)

    def test_select_project(self):

        r = db.get_relation("students")
        request = Select(Project(r, "name"), "name", "Loic")

        # Expected result
        dtypes = {'name': 'text'}
        data = 'Loic'
        rel = Rel(dtypes, data)

        self.assertTrue(request.result == rel)

    def test_rename_project(self):

        r = db.get_relation("students")
        request = Rename(Project(r, "name"), "name", "Name")

        # Expected result
        dtypes = {"Name":"text"}
        data = [['Adrien'], ['Loic']]
        rel = Rel(dtypes, data)

        self.assertTrue(request.result == rel)

    def test_project_rename(self):

        r = db.get_relation("students")
        request = Project(Rename(r, "studies", "Studies"), ["name", "Studies"])

        # Expected result
        dtypes = {'name': 'text', 'Studies': 'text'}
        data = [['Adrien', 'Computer Science'],
                ['Loic', 'Engineering']]
        rel = Rel(dtypes, data)

        self.assertTrue(request.result == rel)

    def test_union_select(self):

        # Expected result
        r = db.get_relation("students")

        request = Union(Select(r, "name", "Adrien"), Select(r, "name", "Loic"))

        self.assertTrue(request.result == r)

    def test_union_select2(self):

        # Expected result
        r = db.get_relation("students")

        request = Union(Select(r, "name", "Adrien"), r)

        self.assertTrue(request.result == r)

    def test_difference_select(self):

        r = db.get_relation("students")
        request = Difference(r, Select(r, "name", "Adrien"))

        #Expected result
        dtypes = {'id': 'integer', 'name': 'text', 'age': 'int', 'studies': 'text'}
        data = [(2, 'Loic', 20, 'Engineering')]
        rel = Rel(dtypes, data)

        self.assertTrue(request.result == rel)


if __name__ == "__main__":

    unittest.main()
