# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from news.models import NewsArticle, NewsOrganisation


class NewsScraperPipeline:
    def process_item(self, item, spider):
        
        source = NewsOrganisation.objects.get(name='The Guardian')

        if len(item['heading']) > 5:
            if len(item['article_address']) > 5:
                if len(item['snippet']) > 10:
                    if len(item['author']) < 1:
                        item['author'] = ''
                    else:
                        item['author'] = item['author'][0]      
                    try:
                        check_article = NewsArticle.objects.get(article_address=item['article_address'])
                        DropItem(item)
                    except NewsArticle.DoesNotExist:
                        article = NewsArticle(
                            news_organisation=source, 
                            article_address=item['article_address'],
                            heading=item['heading'],
                            snippet=item['snippet'],
                            author=item['author'],
                            image_source=item['image_source'],
                            )
                        article.save()
        
        DropItem(item)

       
