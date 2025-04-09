import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.downloadermiddlewares.robotstxt import RobotsTxtMiddleware
import sqlite3

class MySpider(CrawlSpider):
    name = 'my_spider'
    allowed_domains = ['']
    start_urls = ['']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.conn = sqlite3.connect('scrapy_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY,
                url TEXT,
                title TEXT,
                meta_description TEXT
            )
        ''')
        self.conn.commit()

    def parse_item(self, response):
        title = response.xpath('//title/text()').get()
        meta_description = response.xpath('//meta[@name="description"]/@content').get()
        self.cursor.execute('''
            INSERT INTO pages (url, title, meta_description) VALUES (?, ?, ?)
        ''', (response.url, title, meta_description))
        self.conn.commit()

    """def close(self, reason):
        self.conn.close()"""

# Enable robots.txt middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
}
