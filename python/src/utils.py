import sqlite3

class Database:
    """
    Utility class, it wraps around sqlite3 to give
    some useful functions to work with an SQLite
    database.

    You call it with a file path, if the database
    exists, you connect to it. If not, a new database
    will be created at the file path given.

    """

    def __init__(self, database_file_path):
        self.connection = sqlite3.connect(database_file_path)
        self.cursor = self.connection.cursor()


    def get_datatypes(self, table_name):
        """
        Returns the name and datatype of each column
        as a python dictionnary
        """

        self.cursor.execute("pragma table_info({})".format(table_name))
        table_info = self.cursor.fetchall()
        dic = {}

        for row in table_info:
            dic[row[1]] = row[2] # row[1] = col_name, row[2] = data_type

        return dic

    def get_columns(self, table_name, columns=None):
        """
        Function to retrieve the columns of a table. If you only provide the
        table name, you get all the columns associated to it.

        The columns keyword is an array of strings containing the columns
        name. They all must be correctly written.

        Example :

        Table gpus

        | GpuName         | Price| Availability |
        | Nvidia RTX 3070 |  499$| 0            |
        | Nvidia RTX 3080 |  699$| 0            |
        | Nvidia RTX 3090 | 1499$| 1            |

        >>> db = Database("path_to_db")
        >>> db.get_columns(gpus)

        | Nvidia RTX 3070 |  499$| 0 |
        | Nvidia RTX 3080 |  699$| 0 |
        | Nvidia RTX 3090 | 1499$| 1 |

        >> db.get_columns(gpus, columns=["GpuName", "Availability"])

        | Nvidia RTX 3070 | 0 |
        | Nvidia RTX 3080 | 0 |
        | Nvidia RTX 3090 | 1 |
        """

        if columns == None:
            self.cursor.execute("SELECT * FROM {}".format(table_name))
        else:
            names = ", ".join(columns)
            self.cursor.execute("SELECT {} FROM {}".format(names, table_name))

        return self.cursor.fetchall()
