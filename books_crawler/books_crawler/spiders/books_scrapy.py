# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import os
import glob

from books_crawler.items import BooksCrawlerItem
from scrapy.loader import ItemLoader


def product_info(response, value):
    return response.xpath('//th[text()="'+value+'"]/following-sibling::td/text()').extract_first()


class BooksScrapySpider(scrapy.Spider):
    name = 'books_scrapy'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # def __init__(self, category):
    #     self.start_urls = [category]

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            url = response.urljoin(book)
            yield Request(url, callback=self.parse_book)

        next_page_url = response.xpath(
            "//a[text()='next']/@href").extract_first()
        absolute_next_page = response.urljoin(next_page_url)
        yield Request(absolute_next_page)

    def parse_book(self, response):
        l = ItemLoader(item=BooksCrawlerItem(), response=response)

        title = response.css("h1::text").extract_first()
        price = response.xpath(
            "//*[@class='price_color']/text()").extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')
        rating = response.xpath(
            "//*[contains(@class,'star-rating')]/@class").extract_first()

        rating = rating.replace("star-rating", '')
        description = response.xpath(
            "//*[@id='product_description']/following-sibling::p/text()").extract_first()

        upc = product_info(response, 'UPC')
        product_type = product_info(response, 'Product Type')
        price_without_tax = product_info(response, 'Price (excl. tax)')
        price_with_tax = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of reviews')

        url = response.request.url

        l.add_value('title', title)
        l.add_value('price', price)
        l.add_value('image_urls', image_url)
        yield l.load_item()
        yield {'title': title,
               'price': price,
               'rating': rating,
               'image_url': image_url,
               'description': description,
               'upc': upc,
               'product_type': product_type,
               'price_without_tax': price_without_tax,
               'price_with_tax': price_with_tax,
               'tax': tax,
               'availability': availability,
               'number_of_reviews': number_of_reviews,
               'url': url}

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'foobar.csv')
