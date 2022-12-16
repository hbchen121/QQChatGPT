# encoding: utf-8
import json
import time
import random
import asyncio
from nonebot import on_message, on_notice
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .config import Config
from .time_control import TimeControl
from .response_for_common_user import get_response_for_common_user

"""
参考Chat插件并进行修改: https://blog.csdn.net/starvapour/article/details/120155711,
其包含关键词回复和戳一戳回复，这里删除戳一戳，仅保留自动回复。
"""

__plugin_name__ = 'chat'
__plugin_usage__ = '用法： '

DEBUG = True

tc = TimeControl(config=Config)
chat = on_message(priority=Config.priority)


# 针对聊天信息
@chat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    begin_time = time.time()
    # 上次响应时间
    ids = event.get_session_id()
    # 只对于群聊信息进行响应
    if ids.startswith("group"):
        # 拆解得到群号与用户号
        _, group_id, user_id = event.get_session_id().split("_")
        is_super_user = user_id in Config.super_uid

        # 消息参考: https://v2.nonebot.dev/docs/tutorial/process-message
        message = event.get_message()
        text_msg = ""

        # 通过 is_tome 判断是否被 at
        at_me = event.is_tome()
        # print("===> at_me:", at_me)
        # print("===>", message)
        for msg in message:
            # print("===>", msg.type, msg.data)
            if msg.type == "at":
                if msg.data.get("qq", "") == Config.bot_id:
                    at_me = True
            elif msg.type == "text":
                text = msg.data["text"]
                text_msg += text + "\n"
        if not at_me or text_msg == "":
            return

        # 只对位于启用列表内的群组和非bot自身发送的信息进行响应
        if group_id in Config.used_in_group and user_id != Config.bot_id:

            # # 1. 执行超级用户信息处理
            # # 超级用户无视冷却cd，也不会重置冷却cd
            # if is_super_user:
            #     response = await get_response_for_super_user()
            #     # 如果回应不为空
            #     if response:
            #         # 发送响应字符串
            #         await chat.finish(response)

            # # 2. 执行无冷却cd的违禁信息检查，忽略超级用户
            # if user_id not in Config.super_uid:
            #     response = await get_response_for_banned(bot=bot, user_id=user_id, group_id=group_id,
            #                                              default_ban_time=Config.default_ban_time)
            #     # 如果回应不为空
            #     if response:
            #         # 发送响应字符串
            #         await chat.finish(response)

            # 3. 执行普通用户信息处理，如果超级用户的响应为空，也要进入这一步
            # 用户是否为超级用户
            response = await get_response_for_common_user(text_msg, group_id, is_super_user, tc)
            # 如果回应不为空
            if response:
                # print("==> runtime: ", time.time() - begin_time)
                if time.time() - begin_time < Config.sleep_time[0]:
                    # 随机睡一会，防止被检测
                    await asyncio.sleep(random.uniform(*Config.sleep_time))
                # 发送响应字符串
                await chat.finish(response)


