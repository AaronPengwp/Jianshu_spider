# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse


class SeleniumDownloadMiddlewares(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'/home/pwp/PycharmProjects/chromedriver')

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)  # 防止网页还没加载完成
        try:
            while True:
                showMore = self.driver.find_element_by_class_name('show-more')
                showMore.click()
                time.sleep(0.3)
                if not showMore:
                    break
        except:#处理页面的专题时没有‘展开更多’选项时发生的异常,不程序就报错了
            pass

        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8') #把source封装成response返回给爬虫解析

        return response
