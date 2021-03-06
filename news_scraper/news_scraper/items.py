# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()
    heading = scrapy.Field()
    article_address = scrapy.Field()
    snippet = scrapy.Field()
    published_date = scrapy.Field()
    author = scrapy.Field()
    image_source = scrapy.Field()
    category = scrapy.Field()
