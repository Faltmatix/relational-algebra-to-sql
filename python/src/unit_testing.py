import unittest
from query import *
from operators import *

class TestQuery(unittest.TestCase):

    def test_init_not_string(self):
        self.assertRaises(TypeError, Query(100))

    def test_init_not_database(self):
        self.assertRaises(BaseException, Query("Abcd"))

    def test_init_file_not_found(self):
        self.assertRaises(FileNotFoundError, Query("database.db"))

#class TestSelect(unittest.TestCase):
#class TestProject(unittest.TestCase):
#class TestJoin(unittest.TestCase):
#class TestRename(unittest.TestCase):
#class TestUnion(unittest.TestCase):
#class TestDifference(unittest.TestCase):

if __name__ == "__main__":
    assert(BaseException == Query("Abcd"))
#    unittest.main()
