import utils

class Operator:
    """This class is the template of the operators.
       Functions that should be available to all
       the operators are put here. The class itself
       should not be called"""

    # The columns names should be strings inside a tuple or list
    authorized_types = [str, list, tuple]

    def __init__(self):
        """"""

    def check_cols(self, cols):

        cols_type = type(cols)

        if cols_type not in Operator.authorized_types:
            raise TypeError("""You entered the wrong type of argument for the
                               columns_name of {} \nIt should be either
                               a string for selecting one column and it
                               should be a tuple or a list of strings for
                               selecting multiple columns but the argument
                               received
                               is : {}""".format(self.__str__, cols_type))

        if cols_type == list or cols_type == tuple:
            for column_name in cols:
                if type(column_name) != str:
                    raise TypeError("""The members from your collection
                                       should be strings, but {} is
                                       {}""".format(column_name,
                                                    type(column_name)))
    def is_atomic(self, table):
        ttype = type(table)
        return ttype == list or ttype == tuple


class Select(Operator):

    def __init__(self, columns_name, table):
        """Cols should be put in a tuple (*cols,)
           to prevent SQL injection from the string operations"""

        self.cols = self.check_cols(columns_name)


class Project(Operator):

    def __init__(self, column_names, table):
        """"""
        self.is_atomic = self.is_atomic(table)


    def execute_op(self):
        """"""
       
class Join:

    def __init__(self):
        """"""
        super().__init__()

class Rename:

    def __init__(self):
        """"""
        super().__init__()

class Union:

    def __init__(self):
        """"""
        super().__init__()

class Difference:

    def __init__(self):
        """"""
        super().__init__()


class Rel:

    """
    Rel is a relation from some database. You can either
    instatiate it with the help of utils.Database or
    you can simply create a relation where
    dtypes is a dictionnary of the columns name and
    data is a list of tuples with the length of the dictionnary

    It is recommanded to rely more on the Database
    class when calling Rel because it takes care
    of the boilerplate code

    >>> db = utils.Database("path_to_database")
    >>> dtypes  = db.get_datatypes("table_name")
    >>> data = db.get_columns("table_name")
    >>> r = Rel(dtypes, data)
    """

    def __init__(self, dtypes, data):
        self.dtypes = dtypes
        self.data = data
