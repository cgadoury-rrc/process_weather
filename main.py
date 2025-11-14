""" Module Imports. """
from plot_operations.plot_operations import PlotOperations
from scrape_weather.scrape_weather import WeatherScraper
from db_operations.db_operations import DbOperations
from db_context.dcbm import DBCM

def main():
    """ The main method. """
    my_scraper = WeatherScraper()
    my_scraper.scrape_all()

    weather_data = my_scraper.get_weather()

    with DBCM("weather.sqlite") as cur:
        db = DbOperations(cur, weather_data)
        db.purge_data()
        db.save_data()
        plot_ops = PlotOperations(db.fetch_data())
        plot_ops.generate_line_plot(2025, 10)


if __name__ == "__main__":
    main()
