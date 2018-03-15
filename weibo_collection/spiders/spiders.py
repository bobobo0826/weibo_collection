# encoding=utf-8
import re
import json
import datetime
import time
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from weibo_collection.items import WeiboCollectionItem


class Spider(CrawlSpider):
    name = "weibo_collection"
    host = "https://weibo.cn"
    start_urls = "https://weibo.cn/fav/"

    def start_requests(self):
        url= "https://weibo.cn/fav/"
        yield Request(url=url, callback=self.parse)  # 去爬微博


    def parse(self, response):
        """ 抓取微博收藏数据 """
        selector = Selector(response)
        tweets = selector.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            item = WeiboCollectionItem()
            original = dict()
            basic =dict()
            url = response.url
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            _id = tweet.xpath('@id').extract_first()  # 微博ID
            name =tweet.xpath('div[1]/a[@class="nk"]/text()').extract_first()
            forward = tweet.xpath('div[1]/span[1]/text()').extract_first()
            content_type = 0
            if "转发了" in forward:
                content_type = 1 #1为转发，0为原创
                original_name = tweet.xpath('div[1]/span[1]/a/text()').extract_first()
                original_content = tweet.xpath('div/span[@class="ctt"]/text()').extract()  # 微博内容
                original_comment = re.findall(u'\u539f\u6587\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 原文评论数
                content = tweet.xpath('div[3]/text()[1]').extract()  # 微博内容
                if original_comment:
                    original["original_comment"] = int(original_comment[0])
                if original_name:
                    original["original_name"] = original_name
                if original_content:
                    original["original_content"] = original_content
            else:
                content = tweet.xpath('div/span[@class="ctt"]/text()').extract()  # 微博内容

            picture = tweet.xpath('div[1]/a[2]/@href').extract_first()
            like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
            transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
            comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
            others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）
            if _id:
                basic["ID"] = _id
            if name:
                basic["nickName"] = name
            if picture:
                basic["picture"] = picture
            if content:
                basic["content"] = content
            if like:
                if len(like) > 1:
                    basic["like"] = int(like[1])
                    original["like"] = int(like[0])
                else:
                    basic["like"] = int(like[0])
            if transfer:
                if len(transfer) > 1:
                    basic["transfer"] = int(transfer[1])
                    original["transfer"] = int(transfer[0])
                else:
                    basic["transfer"] = int(transfer[0])
            if comment:
                basic["comment"] = int(comment[0])
            if others:
                basic["others"] = others
            if len(original)>1:
                original_info = json.dumps(original, ensure_ascii=False)
                item["original_info"] = original_info
            basic_info = json.dumps(basic, ensure_ascii=False)
            item["basic_info"] = basic_info
            item["content_type"] = content_type
            item["start_time"] = start_time
            item["url"] = url

            yield item
        url_next = selector.xpath('//*[@id="pagelist"]/form/div/a/@href').extract()  # 下页
        if url_next:
            # print("url_next==================")
            # print(url_next)
            # print(self.host + url_next[0])
            yield Request(url=self.host + url_next[0], callback=self.parse)
