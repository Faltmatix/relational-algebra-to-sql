import unittest
from operators import *
import utils

db = utils.Database("../resources/testing.db")

#class TestQuery(unittest.TestCase):

#class TestSelect(unittest.TestCase):
#
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

#class TestJoin(unittest.TestCase):
#class TestRename(unittest.TestCase):
#class TestUnion(unittest.TestCase):
#class TestDifference(unittest.TestCase):

if __name__ == "__main__":

    unittest.main()
