""" Module Imports. """
import sqlite3

class DbOperations:
    """ A class to handle db operations. """
    def __init__(self, weather_data: dict):
        self.initialize_db()
        self._weather_data = weather_data

    def fetch_data(self):
        """ Returns the requested data for plotting. """


    def save_data(self):
        """ Saves new data to the db. """

    def initialize_db(self):
        """ Initializes the database. """
        self._conn = sqlite3.connect("weather.sqlite")
        cur = self._conn.cursor()

        sql = """"""

        cur.execute
