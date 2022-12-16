# encoding: utf-8
class Config:
    # 记录在哪些群组中使用
    used_in_group = ["628779786"]
    # 插件执行优先级
    priority = 10
    # 接话冷却时间（秒），在这段时间内不会连续两次接话
    chat_cd = 0
    # 戳一戳冷却时间（秒）
    notice_cd = 900
    # 机器人QQ号
    bot_id = "2562406934"
    # 管理员QQ号，管理员无视冷却cd和触发概率
    super_uid = ["1085177243"]
    # 聊天回复概率，用百分比表示，0-100%
    p_chat_response = 1
    # 戳一戳回复概率，用百分比表示，0-100%
    p_poke_response = 0
    # 默认禁言时间，每多戳一次会在默认禁言时间上翻倍
    default_ban_time = 60

    # 防止被检测到，回复消息时随机睡眠
    sleep_time = (1, 2)

