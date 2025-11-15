""" Module Imports. """
import sys
from datetime import datetime
from menu import Menu
from db_context.dcbm import DBCM
from db_operations.db_operations import DbOperations
from scrape_weather.scrape_weather import WeatherScraper
from plot_operations.plot_operations import PlotOperations

class WeatherProcessor:
    """ A gui class to process weather data. """
    def __init__(self):
        """ Initializes a new instance of Weather Processor.  """
        self._choice = None
        self._year_range = None
        self._weather_scraper = WeatherScraper()
        self._db_name = "weather.sqlite"

        self.create_start_menu()
        self._main_menu.open()

    def create_start_menu(self):
        """ Create the initial menu that the user sees. """
        self._main_menu = Menu(
            title="Weather Processor",
            options=[
                ("Exit", self.exit_app),
                ("Download Weather Data", self.download_weather_data),
                ("Update Weather Data", self.update_weather_data),
                ("Generate Box Plot", self.generate_box_plot),
                ("Generate Line Plot", self.generate_line_plot)
            ]
        )

    def get_user_date_values(self, is_box_plot:bool = False):
        """ Get the year range input from the user. """
        prompt = ("Enter a start and end year (i.e. 2022 - 2024): " if is_box_plot
                  else "Enter a year and month (i.e. 2025 - 11): ")
        values = input(prompt)
        value_1 = values.split("-")[0].strip()
        value_2 = values.split("-")[1].strip()

        return (value_1, value_2)

    def download_weather_data(self):
        """ Download a full set of weather data. """
        self._weather_scraper.scrape_all()
        weather_data = self._weather_scraper.get_weather()

        with DBCM(self._db_name) as cur:
            database = DbOperations(cur)
            database.purge_data()
            database.save_data(weather_data=weather_data)

    def update_weather_data(self):
        """ 
        Updates weather data from today's date to the 
        most recent date in the db.
        """
        new_data_to_insert = {}
        date_pattern = "%Y-%m-%d"
        self._weather_scraper.scrape_all()
        new_data = self._weather_scraper.get_weather()

        with DBCM(self._db_name) as cur:
            database = DbOperations(cur)
            most_recent_entry = database.fetch_data()[-1][0]
            most_recent_date = datetime.strptime(most_recent_entry, date_pattern)

            for date_string, values in new_data.items():
                if (
                    datetime.strptime(date_string, date_pattern) > most_recent_date
                    ):
                    new_data_to_insert[date_string] = values

            database.save_data(weather_data=new_data_to_insert)

    def generate_box_plot(self):
        """ Generate a box plot for a range of years. """
        with DBCM(self._db_name) as cur:
            db = DbOperations(cur)
            plot_operations = PlotOperations(db.fetch_data())
            year_range = self.get_user_date_values(True)
            plot_operations.show_box_plot(
                int(year_range[0]),
                int(year_range[1])
                )

    def generate_line_plot(self):
        """ Generate a line plot for a specific year and month. """
        with DBCM(self._db_name) as cur:
            db = DbOperations(cur)
            plot_operations = PlotOperations(db.fetch_data())
            year_month = self.get_user_date_values()
            plot_operations.show_line_plot(
                int(year_month[0]),
                int(year_month[1])
                )

    def exit_app(self):
        """ Exit the applications. """
        sys.exit()
