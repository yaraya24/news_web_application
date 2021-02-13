from scrapy import Spider, Request
from scrapy.selector import Selector
from news_scraper.items import NewsScraperItem

class GuardianSpider(Spider):
    name = 'guardian_spider'
    allowed_domains = ["www.theguardian.com"]
    start_urls = [
        "https://www.theguardian.com/international"
    ]
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    

    def parse(self, response):
        articles = Selector(response).xpath('//div[@class="fc-item__header"]/h3')

        for article in articles[:15]:
            item = NewsScraperItem()
            url = article.xpath('a/@href').extract()[0]
            item["article_address"] = url
            if len(url) < 10 == False:
                break
            yield Request(url, callback = self.guardian_article)

    
    def guardian_article(self, response):
        item = NewsScraperItem()
        item['heading'] = response.xpath('//h1/text()').extract()[0].strip()
        item['article_address'] = response.url
        item['snippet'] = response.xpath('/html/body/section[1]/div/div/div[9]/main/main/div[1]/div/p[1]/text()').extract()
        if len(item['snippet']) < 5:
            item['snippet'] = response.xpath('//p/text()').extract()[0]
        item['image_source'] = response.xpath('//img/@src').extract()[1]
        item['author'] = response.xpath('//a[@rel="author"]/text()').extract()
        if not item['author']:
            item['author'] = response.xpath('//a[@rel="author"]/span/text()') 
        yield item
    
