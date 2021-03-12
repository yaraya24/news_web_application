# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    """Class that defines the item passed to the pipeline"""
    
    source = scrapy.Field()
    heading = scrapy.Field()
    article_address = scrapy.Field()
    snippet = scrapy.Field()
    published_date = scrapy.Field()
    author = scrapy.Field()
    image_source = scrapy.Field()
    category = scrapy.Field()
