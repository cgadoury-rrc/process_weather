""" Module Imports. """
from datetime import datetime
import matplotlib.pyplot as plt

class PlotOperations():
    """ A class to plot weather data. """
    def __init__(self, weather_data):
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
                print(f"Warning: Skipping invalid row: {row} - {e}")

        months = sorted(plot_data.keys())
        temps_by_month = [plot_data[month] for month in months]

        plt.boxplot(temps_by_month, labels=months)
        plt.xlabel('Month')
        plt.ylabel('Temperature (C)')
        plt.title('Monthly temperature distribution for: ')

        plt.show()

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
                print(f"Warning: Skipping invalid row: {row} - {e}")

        date_temps = dict(
            sorted(date_temps.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d"))
            )

        plt.plot(date_temps.keys(), date_temps.values())
        plt.xlabel('Day of Month')
        plt.ylabel('Avg Daily Temp')
        plt.title('Daily Avg Temperatures')
        plt.xticks(rotation=45)
        plt.grid(True)

        plt.show()
