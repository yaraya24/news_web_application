from scrapy import Spider, Request
from scrapy.selector import Selector
from news_scraper.items import NewsScraperItem

class NPRSpider(Spider):
    name = 'npr_spider'

    start_urls = [
        "https://www.npr.org/sections/news/",
        "https://www.npr.org/sections/business/",
        "https://www.npr.org/sections/technology/",
    ]
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        articles = Selector(response).xpath('//h2[@class="title"]')

        category = {
        "https://www.npr.org/sections/news/": "General",
        "https://www.npr.org/sections/business/": "Business",
        "https://www.npr.org/sections/technology/": "Technology",
        }

        for article in articles:
            url = article.xpath('a/@href').extract()[0]
            yield Request(url, callback = self.npr_article, meta={'category': category[response.url]})

    def npr_article(self, response):
        item = NewsScraperItem()
        item['source'] = 'NPR'
        item['category'] = response.meta.get('category')
        item['heading'] = response.xpath('string(//h1)').get().strip()
        item['article_address'] = response.url
        item['snippet'] = response.xpath('string(//div[@class="storytext"]/p[1])').get()
        if len(item['snippet']) < 15:
            item['snippet'] = response.xpath('string(//p[2])').get()
        try:
            item['image_source'] = response.xpath('//div[@class="bucketwrap image large"]/div[1]/img/@src').extract()[0]
        except:
            item['image_source'] = "https://play-lh.googleusercontent.com/iV4u7kqNEyTbMI2Di7MXR5VyP2wZelmW2JcCqYQwwt0L4uP7AKq37T5FQ2O0XUXxXi4"
        item['author'] = response.xpath('string(//p[@class="byline__name byline__name--block"])').get().strip()

        yield item