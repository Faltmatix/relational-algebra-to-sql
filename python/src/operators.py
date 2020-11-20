#!/usr/bin/env python3

class Operator:
    """This class is the template of the operators.
       Functions that should be available to all
       the operators are put here. The class itself
       should not be called"""

    authorized_types = [str, list, tuple]

    def __init__(self):
        """"""

    def check_cols(cols):

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

        return cols


class Select(Operator):

    def __init__(self, columns_name, table):
        """Cols should be put in a tuple (*cols,)
           to prevent SQL injection from the string operations"""

        self.cols = self.check_cols(columns_name)


class Project:

    def __init__(self):
        """"""
        super().__init__()

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
