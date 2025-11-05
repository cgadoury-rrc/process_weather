""" Module Imports. """
from sqlite3 import Cursor

class DbOperations:
    """ A class to handle db operations. """
    def __init__(self, cursor: Cursor, weather_data: dict[str: dict]):
        self._cur = cursor
        self._weather_data = weather_data
        self.rows = []
        self.initialize_db()

    def fetch_data(self):
        """ Returns the requested data for plotting. """
        sql = """
              select sample_date, location, min_temp, max_temp, avg_temp 
              from weather 
              order by sample_date
              """

        return self._cur.execute(sql).fetchall()

    def save_data(self):
        """ Saves new data to the db. """
        for sample_date, temps in self._weather_data.items():
            sql = """
                  insert or ignore into weather (sample_date, location, min_temp, max_temp, avg_temp)
                  values (?, ?, ?, ?, ?)
                  """
            values = (sample_date, "Winnipeg, MB", temps["Min"], temps["Max"], temps["Mean"])

            self._cur.execute(sql, values)

    def initialize_db(self):
        """ Initializes the database. """
        sql = """
                create table if not exists weather
                (
                id integer primary key autoincrement not null,
                sample_date text,
                location text,
                min_temp real, 
                max_temp real, 
                avg_temp real,
                unique(sample_date, location)
                )
              """

        self._cur.execute(sql)

        print("Table created successfully.")

    def purge_data(self):
        """ Deletes data from the database. """
        sql = """
              delete from weather
              """

        self._cur.execute(sql)
