# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request









class ImageSpiderPipeline(ImagesPipeline):


    def process_item(self, item, spider):
        return item


    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:

            yield Request(image_url)


    def item_completed(self, results, item, info):
        image_paths = [info['/Users/lilith/Documents/Praktikum-Uni/images/saved'] for success, info in results if success]


        if not image_paths:
            raise DropItem("Item contains no images")

        item['image_paths'] = image_paths

        return item



