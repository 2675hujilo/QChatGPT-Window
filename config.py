# 配置文件: 注释里标[必需]的参数必须修改, 其他参数根据需要修改, 但请勿删除
import logging
 
mirai_http_api_config = {
    "adapter": "WebSocketAdapter",
    "host": "localhost",
    "port": 10081,
    "verifyKey": "yirimirai",
    "qq": 2675174581
}

openai_config = {
    "api_key": {
        "default": "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"
    },
    "http_proxy": None,
    "reverse_proxy": None
}

admin_qq = 3225373939

default_prompt = {
    "default": "如果我之后想获取帮助，请你说“输入!help获取帮助”",
}

preset_mode = "normal"

response_rules = {
    "at": True,  # 是否响应at机器人的消息
    "prefix": ["/ai", "!ai", "！ai", "ai"],
    "regexp": [],  # "为什么.*", "怎么?样.*", "怎么.*", "如何.*", "[Hh]ow to.*", "[Ww]hy not.*", "[Ww]hat is.*", ".*怎么办", ".*咋办"
    "random_rate": 0.0,  # 随机响应概率，0.0-1.0，0.0为不随机响应，1.0为响应所有消息, 仅在前几项判断不通过时生效
}

ignore_rules = {
    "prefix": ["/"],
    "regexp": []
}

income_msg_check = False

sensitive_word_filter = True

baidu_check = False

baidu_api_key = ""

baidu_secret_key = ""

inappropriate_message_tips = "[百度云]请珍惜机器人，当前返回内容不合规"

encourage_sponsor_at_start = False

prompt_submit_length = 2048

# 现已支持的模型有：
# 
#    'gpt-4'
#    'gpt-4-0314'
#    'gpt-4-32k'
#    'gpt-4-32k-0314'
#    'gpt-3.5-turbo'
#    'gpt-3.5-turbo-0301'
#    'text-davinci-003'
#    'text-davinci-002'
#    'code-davinci-002'
#    'code-cushman-001'
#    'text-curie-001'
#    'text-babbage-001'
#    'text-ada-001'
#
completion_api_params = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.9,  # 数值越低得到的回答越理性，取值范围[0, 1]
    "top_p": 1,  # 生成的文本的文本与要求的符合度, 取值范围[0, 1]
    "frequency_penalty": 0.2,
    "presence_penalty": 1.0,
}

image_api_params = {
    "size": "256x256",  # 图片尺寸，支持256x256, 512x512, 1024x1024
}

# 群内回复消息时是否引用原消息
quote_origin = True

# 回复绘图时是否包含图片描述
include_image_description = True

# 消息处理的超时时间，单位为秒
process_message_timeout = 60

# 回复消息时是否显示[GPT]前缀
show_prefix = False

# 应用长消息处理策略的阈值
# 当回复消息长度超过此值时，将使用长消息处理策略
blob_message_threshold = 256

# 长消息处理策略
# - "image": 将长消息转换为图片发送
# - "forward": 将长消息转换为转发消息组件发送
blob_message_strategy = "forward"

# 文字转图片时使用的字体文件路径
# 当策略为"image"时生效
#   若在Windows系统下，程序会自动使用Windows自带的微软雅黑字体
#   若未填写或不存在且不是Windows，将禁用文字转图片功能，改为使用转发消息组件
font_path = ""

# 消息处理超时重试次数
retry_times = 3

# 消息处理出错时是否向用户隐藏错误详细信息
# 设置为True时，仅向管理员发送错误详细信息
# 设置为False时，向用户及管理员发送错误详细信息
hide_exce_info_to_user = False



# 线程池相关配置
# 该参数决定机器人可以同时处理几个人的消息，超出线程池数量的请求会被阻塞，不会被丢弃
# 如果你不清楚该参数的意义，请不要更改
# 程序运行本身线程池，无代码层面修改请勿更改
sys_pool_num = 8

# 执行管理员请求和指令的线程池并行线程数量，一般和管理员数量相等
admin_pool_num = 2

# 执行用户请求和指令的线程池并行线程数量
# 如需要更高的并发，可以增大该值
user_pool_num = 6

# 每个会话的过期时间，单位为秒
# 默认值20分钟
session_expire_time = 60 * 20

# 会话限速
# 单会话内每分钟可进行的对话次数
# 若不需要限速，可以设置为一个很大的值
# 默认值60次，基本上不会触发限速
rate_limitation = 60

# 会话限速策略
# - "wait": 每次对话获取到回复时，等待一定时间再发送回复，保证其不会超过限速均值
# - "drop": 此分钟内，若对话次数超过限速次数，则丢弃之后的对话，每自然分钟重置
rate_limit_strategy = "drop"


# 是否在启动时进行依赖库更新
upgrade_dependencies = False

# 是否上报统计信息
# 用于统计机器人的使用情况，不会收集任何用户信息
# 仅上报时间、字数使用量、绘图使用量，其他信息不会上报
report_usage = True

# 日志级别
logging_level = logging.INFO

