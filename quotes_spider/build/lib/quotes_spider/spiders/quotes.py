# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy import Spider
from quotes_spider.items import QuotesSpiderItem

class QuotesSpider(Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # h1_tags = response.xpath('//h1/a/text()').extract_first()
        # tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        # yield {'H1 Tag': h1_tags, 'Tags':tags}

        l=ItemLoader(item=QuotesSpiderItem(),response=response)

        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath(
                './/*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath(
                './/*[@itemprop="keywords"]/@content').extract_first()
            l.add_value('author',author)
            l.add_value('tags',tags)
            l.add_value('text',text)


            # yield {"Text": text,
            #        "Author": author,
            #        "Tags": tags}
            yield l.load_item()

            next_page_url = response.xpath(
                '//*[@class="next"]/a/@href').extract_first()
            absolute_next_page_url = response.urljoin(next_page_url)

            yield scrapy.Request(absolute_next_page_url)
