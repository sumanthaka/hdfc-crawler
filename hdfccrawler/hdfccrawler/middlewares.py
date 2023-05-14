# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from random import choice
from urllib.parse import urlencode

import requests
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class HeaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # Initialize the ScrapeOps API key and endpoint
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT',
                                               'http://headers.scrapeops.io/v1/browser-headers')
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self.set_headers_list()

    def set_headers_list(self):
        # Get the list of fake browser headers from ScrapeOps
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def random_browser_header(self):
        header = choice(self.headers_list)
        return header

    def process_request(self, request, spider):
        random_browser_header = self.random_browser_header()
        # Change the headers to use the fake browser header
        request.headers['accept-language'] = random_browser_header['accept-language']
        request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user']
        request.headers['sec-fetch-mod'] = random_browser_header['sec-fetch-mod']
        request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
        request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform']
        request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile']
        request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua']
        request.headers['accept'] = random_browser_header['accept']
        request.headers['user-agent'] = random_browser_header['user-agent']
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')

