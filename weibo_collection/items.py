# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field

class WeiboCollectionItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # ID = Field()  # 用户ID-微博ID
    # NickName = Field()  # 昵称
    # Content = Field()  # 微博内容
    # Picture = Field()
    # # PubTime = Field()  # 发表时间
    # # Tools = Field()  # 发表工具/平台
    # Like = Field()  # 点赞数
    # Comment = Field()  # 评论数
    # Transfer = Field()  # 转载数
    # Others = Field()
    url = Field()
    start_time = Field()
    basic_info = Field()
    content_type = Field()
    original_info = Field()

    pass
