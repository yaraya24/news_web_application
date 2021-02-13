from scrapy import Spider, Request
from scrapy.selector import Selector
from news_scraper.items import NewsScraperItem

class GuardianSpider(Spider):
    name = 'guardian_spider'
    allowed_domains = ["www.theguardian.com"]
    start_urls = [
        "https://www.theguardian.com/international",
        "https://www.theguardian.com/uk/culture",
        "https://www.theguardian.com/uk/sport",
        "https://www.theguardian.com/uk/technology",
        "https://www.theguardian.com/uk/business"
    ]
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    

    def parse(self, response):
        articles = Selector(response).xpath('//div[@class="fc-item__header"]/h3')[:15]
        
        category = {
            "https://www.theguardian.com/international": 'Headlines',
            "https://www.theguardian.com/uk/culture": 'Culture',
            "https://www.theguardian.com/uk/sport" : 'Sports',
            "https://www.theguardian.com/uk/technology": 'Technology',
            "https://www.theguardian.com/uk/business" : 'Business'

        }

        
        for article in articles:
            item = NewsScraperItem()
            url = article.xpath('a/@href').extract()[0]
            item["article_address"] = url
            if len(url) < 10 == False:
                break
            yield Request(url, callback = self.guardian_article, meta={'category': category[response.url]})

    
    def guardian_article(self, response):
        item = NewsScraperItem()
        item['category'] = response.meta.get('category')
        item['heading'] = response.xpath('//h1/text()').extract()[0].strip()
        item['article_address'] = response.url
        item['snippet'] = response.xpath('string(/html/body/section[1]/div/div/div[9]/main/main/div[1]/div/p[1])').get()
        if len(item['snippet']) < 5:
            item['snippet'] = response.xpath('string(/html/body/section[1]/div/div/div[9]/main/main/div[1]/div/p[2])').get()
        item['image_source'] = response.xpath('//img/@src').extract()[1]
        item['author'] = response.xpath('string(//a[@rel="author"])').get()
        yield item
    
