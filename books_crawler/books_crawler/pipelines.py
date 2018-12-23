# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os


class BooksCrawlerPipeline(object):
    def process_item(self, item, spider):
        os.chdir('/home/it-grupo/Documentos/scrapy/scrapy_items_example')

        if item['images']:
            if  'path'  in item['images'][0]:
                new_image_name = item['title'][0]
                new_image_path = 'full/'+new_image_name
                os.rename(item['images'][0]['path'],new_image_path)


        return item
