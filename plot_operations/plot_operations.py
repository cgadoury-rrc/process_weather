""" Module Imports. """
import logging
from datetime import datetime
import matplotlib.pyplot as plt

class PlotOperations():
    """ 
    A class to plot weather data. 
    Author: Colton Gadoury
    """
    def __init__(self, weather_data):
        """ Initializes a new instance of Plot Operations. """
        self._weather_data = weather_data

    def generate_box_plot(self, start_year: int, end_year: int) -> None:
        """ Prepare weather data for box plotting.  """
        plot_data: dict[int, list[float]] = {}
        for row in self._weather_data:
            try:
                date_parts = str(row[0]).split('-')
                year = int(date_parts[0])
                month = int(date_parts[1])

                if start_year <= year <= end_year:
                    temp = float(row[4])
                    plot_data.setdefault(month,[]).append(temp)

            except ValueError as e:
                logging.warning("Warning: Skipping invalid row: %s - %s", row, e)

        return plot_data

    def generate_line_plot(self, start_year: int, start_month: int) -> None:
        """ Prepare weather data for line plotting. """
        date_temps = {}
        for row in self._weather_data:
            try:
                date_string = str(row[0])
                date_parts = date_string.split('-')
                year = int(date_parts[0])
                month = int(date_parts[1])

                if year == start_year and month == start_month:
                    temp = float(row[4])
                    date_temps[date_string] = temp

            except ValueError as e:
                logging.warning("Warning: Skipping invalid row: %s - %s", row, e)

        return dict(
            sorted(date_temps.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d"))
            )

    def show_box_plot(self, start_year: int, end_year: int):
        """ Generate and show the box plot to the user. """
        plot_data: dict = self.generate_box_plot(start_year=start_year, end_year=end_year)
        months = sorted(plot_data.keys())
        temps_by_month = [plot_data[month] for month in months]

        plt.boxplot(temps_by_month, labels=months)
        plt.xlabel("Month")
        plt.ylabel("Temperature (C)")
        plt.title(f"Monthly temperature distribution for: {start_year} - {end_year}")

        plt.show()

    def show_line_plot(self, start_year: int, start_month: int):
        """ Generate and show the line plot to the user. """
        plot_data: dict = self.generate_line_plot(start_year=start_year, start_month=start_month)

        plt.plot(plot_data.keys(), plot_data.values())
        plt.xlabel('Day of Month')
        plt.ylabel('Avg Daily Temp')
        plt.title('Daily Avg Temperatures')
        plt.xticks(rotation=45)
        plt.grid(True)

        plt.show()
