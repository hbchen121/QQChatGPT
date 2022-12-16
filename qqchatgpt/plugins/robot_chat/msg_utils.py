# encoding: utf-8
"""
处理 message 的一些有用接口
"""
import os
from typing import Set
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.params import EventMessage

img_path = 'file:///' + os.path.split(os.path.realpath(__file__))[0] + '/img/'


def extract_member_at(message: Message) -> Set[str]:
    """提取消息中被艾特人的QQ号
    参数:
        message: 消息对象
    返回:
        被艾特集合
    """
    return {
        segment.data["qq"]
        for segment in message
        if (segment.type == "at") and ("qq" in segment.data)
    }


async def message_at_rule(event: GroupMessageEvent, message: Message = EventMessage()):
    """
    返回时间
    """
    return extract_member_at(message=message) or event.reply


def send_img(img_name):
    """
    发送图片时用到的函数, 返回发送图片所用的编码字符串
    """
    return MessageSegment.image(img_path + img_name)