from scrapy import Spider, Request
from scrapy.selector import Selector
from news_scraper.items import NewsScraperItem


class ReutersSpider(Spider):
    """ Spider that will scrape for articles from Reuters"""
    name = "reuters_spider"
    start_urls = [
        "https://www.reuters.com/",
        "https://www.reuters.com/business",
        "https://www.reuters.com/technology",
        "https://www.reuters.com/lifestyle",
    ]

    custom_settings = {"DEPTH_LIMIT": 2}

    def parse(self, response):
        """Method to parse articles using Xpaths"""
        articles = Selector(response).xpath('//div[@class="story-content"]')
        category = {
            "https://www.reuters.com/": "General",
            "https://www.reuters.com/business": "Business",
            "https://www.reuters.com/technology": "Technology",
            "https://www.reuters.com/lifestyle": "Culture",
        }

        for article in articles:
            url = "https://www.reuters.com" + article.xpath("a/@href").extract()[0]
            yield Request(
                url,
                callback=self.reuters_article,
                meta={"category": category[response.url]},
            )

    def reuters_article(self, response):
        """Call back method to create a News Article object based on scraped data"""
        item = NewsScraperItem()
        item['source'] = 'Reuters'
        item["category"] = response.meta.get("category")
        item["article_address"] = response.url
        item["heading"] = response.xpath("string(//h1)").get().strip()
        item["snippet"] = (
            response.xpath(
                'string(//p[@class="Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x"])'
            )
            .get()
            .strip()
        )
        item["image_source"] = "https://i1.sndcdn.com/avatars-000334209154-7w0njd-t500x500.jpg"
        item["author"] = (
            response.xpath(
                'string(//a[@class="TextLabel__text-label___3oCVw TextLabel__black-to-orange___23uc0 TextLabel__serif___3lOpX Byline-author-2BSir"])'
            )
            .get()
            .strip()
        )
        yield item