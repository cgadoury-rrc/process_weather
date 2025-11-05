""" Module Imports. """
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
        print(db.fetch_data())

if __name__ == "__main__":
    main()
