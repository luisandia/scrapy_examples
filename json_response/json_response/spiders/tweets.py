# -*- coding: utf-8 -*-
import scrapy
import json


class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['trumptwitterarchive.com']
    start_urls = [
        'http://trumptwitterarchive.com/data/realdonaldtrump/2017.json']

    def parse(self, response):
        jsonreponse = json.loads(response.body.decode('utf-8'))

        for tweet in jsonreponse:
            yield{
                'created_at': tweet['created_at'],
                'id_str': tweet['id_str'],
                'in_reply_to_user_id_str': tweet['in_reply_to_user_id_str'],
                'is_retweet': tweet['is_retweet'],
                'retweet_count': tweet['retweet_count'],
                'source': tweet['source'],
                'text': tweet['text'],
            }
