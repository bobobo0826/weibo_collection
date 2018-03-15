# encoding=utf-8
import random
from weibo_collection.cookies import cookies
from weibo_collection.user_agents import agents


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        cookie = eval(cookie)  # 将str类型的cookie转换成dict
        request.cookies = cookie

