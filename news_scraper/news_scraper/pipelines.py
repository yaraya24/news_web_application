# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class NewsScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if len(adapter.get('heading')) > 5:
            if len(adapter.get('article_address')) > 5:
                if len(adapter.get('snippet')) > 10:
                    return item
        
        DropItem(item)

       
