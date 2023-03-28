# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ModulePipeline:
    def process_item(self, item, spider):
        item['name'] = ''.join(map(lambda x: x.strip(), item.get('name')))
        item['title'] = ''.join(map(lambda x: x.strip(), item.get('title')))
        item['shops'] = ''.join(map(lambda x: x.strip(), item.get('shops')))
        return item
