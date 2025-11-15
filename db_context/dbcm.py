""" Module Imports. """
import sqlite3

class DBCM():
    """ 
    A database context manager class. 
    Author: Colton Gadoury
    """
    def __init__(self, db_name):
        """ Initializes a new instance of DBCM. """
        self._db_name = db_name
        self._conn = None
        self._cur = None

    def __enter__(self):
        """ Returns a cursor to work with the database. """
        self._conn = sqlite3.connect(self._db_name)
        self._cur = self._conn.cursor()
        return self._cur

    def __exit__(self, exc_type, exc_value, exc_trace):
        """ Handles the close event of the context manager. """
        if exc_type:
            self._conn.rollback()
        else:
            self._conn.commit()
        self._conn.close()
