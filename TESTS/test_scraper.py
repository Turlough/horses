import scraper
from datetime import date
import unittest


class TestScraper(unittest.TestCase):

    def test_create_date_list(self):
        start = date(2020, 1, 1)
        end = date(2020, 1, 31)
        result = scraper.create_date_list(start, end)
        self.assertEquals(31, len(result))

    def test_create_date_list(self):
        start = date(2020, 1, 1)
        end = date(2020, 1, 31)
        result = scraper.create_date_list(start, end)
        self.assertEquals('2020-01-02', result[1])

    def test_create_urls(self):
        start = date(2020, 1, 1)
        end = date(2020, 1, 31)
        result = scraper.create_urls(start, end)
        self.assertEquals('https://www.timeform.com/horse-racing/results/2020-01-02', result[1])