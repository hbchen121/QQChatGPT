# encoding: utf-8
"""
主要用来控制运行时间，设置cd，防止无限触发；
"""
from time import time
from random import randint


class TimeControl(object):
    def __init__(self, config):
        self.config = config
        # 记录上一次响应时间
        self.last_response = {}

        # 初始化时间戳， 初始化为开机时间-cd时间
        init_last_response = time() - config.chat_cd
        for g_id in config.used_in_group:
            self.last_response[g_id] = init_last_response

    def cool_down(self, group_id, cd=None):
        """
            判断是否过了响应cd的函数，默认使用配置文件中的cd
            如果已经超过了最短响应间隔，返回True
        """
        if cd is None:
            cd = self.config.chat_cd
        return time() - self.last_response[group_id] >= cd

    def reset_gid(self, group_id):
        """
            重置回复时钟
        """
        self.last_response[group_id] = time()

    def random_response(self, p=None):
        """
            以指定概率p返回True或者False
            用于随机决定是否要回应
            默认值为配置文件中的默认聊天响应概率
        """
        if p is None:
            p = self.config.p_chat_response
        return randint(0, 99) < p
