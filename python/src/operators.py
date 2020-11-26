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
    def is_atomic(self, rel):
        return isinstance(rel, Rel)


class Select(Operator):

    def __init__(self, columns_name, target_values, rel):
        """Cols should be put in a tuple (*cols,)
           to prevent SQL injection from the string operations"""

        self.columns_name = columns_name
        self.target_values = target_values
        self.rel = rel

    def execute(self):
        """"""

    def execute_atomic(self):
        """"""
        equality = zip(self.columns_name, target_values)


    def execute_non_atomic(self):
        """"""

class Project(Operator):

    def __init__(self, column_names, rel):
        """"""
        self.rel = rel
        self.col_names = column_names
        self.execute()

    def execute(self):
        if self.is_atomic(self.rel):
            self.result = self.execute_atomic()
            self.sql = "SELECT DISTINCT {} FROM {}".format(", ".join(self.col_names),
                                                  self.rel.name)
        else:
            self.result = self.execute_non_atomic()

    def execute_atomic(self):
        """
        Returns a new relation which is the projection
        of the column names in the relation given as
        a parameter to the class
        """
        return self.rel.keep(self.col_names)


    def execute_non_atomic(self):
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

    >>> r = Rel(
               {"student_name":"text", "student_age":"int"},
               [["Adrien", 20], ["Joe", 21]]
               )

    It is recommanded to rely more on the Database
    class when calling Rel because it takes care
    of the boilerplate code

    >>> db = utils.Database("path_to_database")
    >>> dtypes  = db.get_datatypes("rel_name")
    >>> data = db.get_columns("rel_name")
    >>> r = Rel(dtypes, data)

    Implementation details :

    Since python 3.6, dictionaries have become insertion
    ordered, it means we can separate the data types from
    the data contained while still knowing which row belongs
    to which datatype/name
    """

    def __init__(self, dtypes, data, name=None):
        self.dtypes = dtypes
        self.data = data
        self.name = name

    def keep(self, column_names):
        """
        Some comment
        """

        new_data = []
        new_keys = {}
        old_keys = list(self.dtypes.keys())
        key_indexes = []

        for name in column_names:
            for i in range(len(old_keys)):
                if name == old_keys[i]:
                    new_keys[name] = self.dtypes[name]
                    key_indexes.append(i)

        for i in range(len(self.data)):
            row = []
            for j in key_indexes:
                row.append(self.data[i][j])
            new_data.append(row)

        return Rel(new_keys, new_data)

    def __str__(self):
        relation_name = "{}\n".format(self.name) if self.name != None else ""
        col_names = "{}\n".format(self.dtypes)
        data = ""
        for i in range(len(self.data)):
            data += "{}\n".format(self.data[i])

        return relation_name + col_names + data


    def __eq__(self, r):
        return self.dtypes == r.dtypes and self.data == r.data
