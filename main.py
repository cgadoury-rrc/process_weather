""" Module Imports. """
from scrape_weather.scrape_weather import WeatherScraper

def main():
    """ The main method. """
    my_scraper = WeatherScraper()
    my_scraper.scrape_all()

    weather_data = my_scraper.get_weather()
    for k, v in weather_data.items():
        print(f"Key: {k}, Value: {v}")

if __name__ == "__main__":
    main()
