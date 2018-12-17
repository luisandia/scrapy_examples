# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        # //*/input[@name="csrf_token"]/@value
        # //*[@name="csrf_token"]/@value
        csrf_token = response.xpath('/html/body/div/form/input[@name="csrf_token"]/@value').extract()
        yield FormRequest('http://quotes.toscrape.com/login', formdata={'csrf_token': csrf_token,
                                                                        'username': '1111', 'password': '111'},
                          callback=self.parse_after_login)
    
    def parse_after_login(self,response):
        if response.xpath('//*/a[text()="Logout"]'):
            self.log("You logged in!!!")

        open_in_browser(response)
