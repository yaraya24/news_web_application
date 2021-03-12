from scrapy import Spider, Request
from scrapy.selector import Selector
from news_scraper.items import NewsScraperItem

class GuardianSpider(Spider):
    """ Spider that will scrape for articles from The Guardian"""
    name = 'guardian_spider'
    
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
        """Method to parse articles using Xpaths"""
        articles = Selector(response).xpath('//div[@class="fc-item__header"]/h3')
        
        category = {
            "https://www.theguardian.com/international": 'General',
            "https://www.theguardian.com/uk/culture": 'Culture',
            "https://www.theguardian.com/uk/sport" : 'Sports',
            "https://www.theguardian.com/uk/technology": 'Technology',
            "https://www.theguardian.com/uk/business" : 'Business'

        }

        
        for article in articles:
            url = article.xpath('a/@href').extract()[0]
            yield Request(url, callback = self.guardian_article, meta={'category': category[response.url]})

    
    def guardian_article(self, response):
        """Call back method to create a News Article object based on scraped data"""
        item = NewsScraperItem()
        item['source'] = "The Guardian"
        item['category'] = response.meta.get('category')
        item['heading'] = response.xpath('string(//h1)').get().strip()
        item['article_address'] = response.url
        item['snippet'] = response.xpath('string(//div[@class="article-body-commercial-selector css-79elbk article-body-viewer-selector"]/p)').get()
        if len(item['snippet']) < 5:
            item['snippet'] = response.xpath('string(/html/body/section[1]/div/div/div[9]/main/main/div[1]/div/p[2])').get()
        item['image_source'] = response.xpath('//img/@src').extract()[1]
        item['author'] = response.xpath('string(//a[@rel="author"])').get()
        yield item