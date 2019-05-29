# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem



class ShortbookSpider(CrawlSpider):
    name = 'shortBook'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://.*/p/[0-9a-w]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="title"]/text()').get()
        avatar = response.xpath('//a[@class="avatar"]/img/@src').get()
        avatar = response.urljoin(avatar)
        author = response.xpath('//span[@class="name"]/a/text()').get()
        pub_time = response.xpath('//span[@class="publish-time"]/text()').get().replace("*", "")
        # https: // www.jianshu.com / p / 277b4af3974e?utm_campaign = maleskine & utm_content = note & utm_medium = seo_notes & utm_source = recommendation
        #https://www.jianshu.com/p/04bae7f523c5

        url = response.url

        # ['https: // www.jianshu.com / p / 277b4af3974e','utm_campaign = maleskine & utm_content = note & utm_medium = seo_notes & utm_source = recommendation']
        #['https://www.jianshu.com/p/04bae7f523c5']

        url = url.split('?')[0]
        article_id = url.split('/')[-1]
        content = response.xpath('//div[@class="show-content"]').get()

        word_count = response.xpath('//span[@class="wordage"]/text()').get()
        read_count = response.xpath('//span[@class="comments-count"]/text()').get()
        comment_count = response.xpath('//span[@class="comments-count"]/text()').get()
        like_count = response.xpath('//span[@class="likes-count"]/text()').get()
        subjects = response.xpath('//div[@class="include-collection"]/a/div/text()').getall() #被以下专题收入

        item = ArticleItem(title=title,author=author,avatar=avatar,pub_time=pub_time,article_id=article_id,content=content,origin_url=response.url,word_count=word_count,read_count=read_count,comment_count=comment_count,like_count=like_count,subjects=subjects)

        yield item


