""" Module Imports. """
import calendar
import datetime
import urllib.request
from html.parser import HTMLParser
from tqdm import tqdm

class WeatherScraper(HTMLParser):
    """ A class to scrape Winnipeg weather data from environment Canada. """

    def __init__(self):
        """ Initializes a new instance of WeatherScraper. """
        super().__init__()
        self._weather = {}
        self._row_values = []
        self._visited = set()
        self._column_index = 0
        self._base_url = "https://climate.weather.gc.ca"
        self._year = None
        self._month = None
        self._current_tag = None
        self._selected_field = None
        self._previous_month_url = None

    def scrape_all(self):
        """ The main scraping method"""
        print("Beginning weather scrape...")

        progress_bar = tqdm(desc="Scraping months", unit=" month")
        url = ('https://climate.weather.gc.ca/climate_data/daily_data_e.html' +
            '?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5')

        while url not in self._visited:
            self._visited.add(url)

            html = self.get_html(url)
            self.feed(html)

            progress_bar.update(1)

            url = self.get_previous_page_url()

        progress_bar.close()

        print("Scrape complete!")


    def handle_starttag(self, tag, attrs):
        """ Handle the start tag. """
        if tag == 'a' and attrs[0][1] == 'prev':
            self._previous_month_url = attrs[1][1]

        elif tag == 'tr':
            self._current_tag = tag

        elif tag == 'select':
            self._current_tag = tag

            for attr in attrs:
                if attr[0] == 'name':
                    self._selected_field = attr[1]

        elif tag == 'option':
            self._current_tag = tag

            if len(attrs) > 1 and attrs[1][0] == 'selected' and self._selected_field:
                if self._selected_field == 'Year':
                    self._year = int(attrs[0][1])
                else:
                    self._month = int(attrs[0][1])


    def handle_endtag(self, tag):
        """ Handles the end of a tag. """
        daily_temps = {}
        temp_headers = ["Max", "Min", "Mean"]

        if self._current_tag == tag and self._row_values:
            day = self._row_values[0]
            days_in_month = calendar.monthrange(self._year, self._month)[1]

            if str(day).isnumeric() and int(day) <= days_in_month:
                date = datetime.date(int(self._year), int(self._month), int(day))

                for index, value in enumerate(self._row_values[1::]):
                    daily_temps[temp_headers[index]] = value

                self._weather[f"{date.year}-{date.month}-{date.day}"] = daily_temps

            self._column_index = 0
            self._row_values = []
            self._current_tag = None


    def handle_data(self, data):
        """ Handle data returned from the response. """
        if self._current_tag == 'tr' and self._column_index < 4:
            try:
                float(data)
                self._row_values.append(data)
                self._column_index += 1
            except ValueError:
                if data == 'M':
                    self._row_values.append(data)
                    self._column_index += 1

        elif self._current_tag == 'select':
            if self._selected_field == 'Year':
                self._year = data
            else:
                self._month = data

    def get_html(self, url):
        """ Gets the html content for a given url. """
        with urllib.request.urlopen(url) as response:
            return str(response.read())

    def get_previous_page_url(self):
        """ Gets the url of the previous page. """
        return self._base_url + self._previous_month_url

    def get_weather(self):
        """ Gets the weather data. """
        return self._weather
