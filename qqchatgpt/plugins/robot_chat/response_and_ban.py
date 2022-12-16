# encoding: utf-8
from collections import Counter
from .msg_utils import send_img


async def get_response_for_banned(bot, group_id, user_id, default_ban_time, **kwargs):
    """
        用于处理任何情况下都需要进行判断的函数
        设置一些条件对某些用户进行禁言
    """
    # words = Counter(msg)
    # 禁言条件
    flag = False
    if flag:
        # 尝试禁言
        try:
            #禁言
            await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=default_ban_time)
            # 如果对方是管理员，那就假装无事发生
        except:
            pass
        return "禁言" + send_img('xx.jpg')

