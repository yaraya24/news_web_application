from scrapy import Spider, Request
from scrapy.selector import Selector
from news_scraper.items import NewsScraperItem


class ConversationSpider(Spider):
    """ Spider that will scrape for articles from The Conversation"""
    name = 'conversation_spider'
    start_urls = [
        "https://theconversation.com/us",
        "https://theconversation.com/us/arts",
        "https://theconversation.com/us/business",
        "https://theconversation.com/us/technology",
    ]
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        """Method to parse articles using Xpaths"""
        articles = Selector(response).xpath('//div[@class="article--header"]/h2')[:15]

        category = {
            "https://theconversation.com/us": "General",
            "https://theconversation.com/us/arts": "Culture",
            "https://theconversation.com/us/business": "Business",
            "https://theconversation.com/us/technology": "Technology",

        }

        for article in articles:
            url = "https://theconversation.com" + article.xpath('a/@href').extract()[0]
            
            yield Request(url, callback = self.conversation_article, meta={'category': category[response.url]})

    def conversation_article(self, response):
        """Call back method to create a News Article object based on scraped data"""
        item = NewsScraperItem()
        item['source'] = "The Conversation"
        item['category'] = response.meta.get('category')
        item['heading'] = response.xpath('string(//div[@class="content-header-block"]/h1)').get().strip()
        item['article_address'] = response.url
        item['snippet'] = response.xpath('string(//div[@itemprop="articleBody"]/p[1])').get()
        if len(item['snippet']) < 25:
            item['snippet']= response.xpath('string(//div[@itemprop="articleBody"]/p[2])').get()
        item['image_source'] = response.xpath('//img/@src').extract()[2]
        item['author'] = response.xpath('string(//span[@class="fn author-name"])').get().strip()

        yield item
