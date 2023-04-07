# 配置文件: 注释里标[必需]的参数必须修改, 其他参数根据需要修改, 但请勿删除
import logging

# [必需] Mirai的配置
# 请到配置mirai的步骤中的教程查看每个字段的信息
# adapter: 选择适配器，目前支持HTTPAdapter和WebSocketAdapter
# host: 运行mirai的主机地址
# port: 运行mirai的主机端口
# verifyKey: mirai-api-http的verifyKey
# qq: 机器人的QQ号
#
# 注意: QQ机器人配置不支持热重载及热更新
mirai_http_api_config = {
    "adapter": "WebSocketAdapter",
    "host": "localhost",
    "port": 8080,
    "verifyKey": "yirimirai",
    "qq": 1234567890
}

# [必需] OpenAI的配置
# api_key: OpenAI的API Key
# http_proxy: 请求OpenAI时使用的代理，None为不使用，https和socks5暂不能使用
# 若只有一个api-key，请直接修改以下内容中的"openai_api_key"为你的api-key
#
# 如准备了多个api-key，可以以字典的形式填写，程序会自动选择可用的api-key
# 例如
# openai_config = {
#     "api_key": {
#         "default": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#         "key1": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#         "key2": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#     },
#     "http_proxy": "http://127.0.0.1:12345"
# }
#
# 现已支持反向代理，可以添加reverse_proxy字段以使用反向代理
# 使用反向代理可以在国内使用OpenAI的API，反向代理的配置请参考
# https://github.com/Ice-Hazymoon/openai-scf-proxy
#
# 反向代理填写示例：
# openai_config = {
#     "api_key": {
#         "default": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#         "key1": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#         "key2": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#     },
#     "reverse_proxy": "http://example.com:12345/v1"
# }
openai_config = {
    "api_key": {
        "default": "openai_api_key"
    },
    "http_proxy": None,
    "reverse_proxy": None
}

# [必需] 管理员QQ号，用于接收报错等通知及执行管理员级别指令
# 支持多个管理员，可以使用list形式设置，例如：
# admin_qq = [12345678, 87654321]
admin_qq = 0

# 情景预设（机器人人格）
# 每个会话的预设信息，影响所有会话，无视指令重置
# 可以通过这个字段指定某些情况的回复，可直接用自然语言描述指令
# 例如:
# default_prompt = "如果我之后想获取帮助，请你说“输入!help获取帮助”"
#   这样用户在不知所措的时候机器人就会提示其输入!help获取帮助
# 可参考 https://github.com/PlexPt/awesome-chatgpt-prompts-zh
#
# 如果需要多个情景预设，并在运行期间方便切换，请使用字典的形式填写，例如
# default_prompt = {
#   "default": "如果我之后想获取帮助，请你说“输入!help获取帮助”",
#   "linux-terminal": "我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。",
#   "en-dict": "我想让你充当英英词典，对于给出的英文单词，你要给出其中文意思以及英文解释，并且给出一个例句，此外不要有其他反馈。",
# }
#
# 在使用期间即可通过指令：
# !reset [名称]
#   来使用指定的情景预设重置会话
# 例如：
# !reset linux-terminal
# 若不指定名称，则使用默认情景预设
#
# 也可以使用指令：
# !default <名称>
#   将指定的情景预设设置为默认情景预设
# 例如：
# !default linux-terminal
# 之后的会话重置时若不指定名称，则使用linux-terminal情景预设
#
# 还可以加载文件中的预设文字，使用方法请查看：https://github.com/RockChinQ/QChatGPT/wiki/%E5%8A%9F%E8%83%BD%E4%BD%BF%E7%94%A8#%E9%A2%84%E8%AE%BE%E6%96%87%E5%AD%97
default_prompt = {
    "default": "如果我之后想获取帮助，请你说“输入!help获取帮助”",
}

# 情景预设格式
# 参考值：默认方式：normal | 完整情景：full_scenario
# 默认方式 的格式为上述default_prompt中的内容，或prompts目录下的文件名
# 完整情景方式 的格式为JSON，在scenario目录下的JSON文件中列出对话的每个回合，编写方法见scenario/default-template.json
#     编写方法请查看：https://github.com/RockChinQ/QChatGPT/wiki/%E5%8A%9F%E8%83%BD%E4%BD%BF%E7%94%A8#%E9%A2%84%E8%AE%BE%E6%96%87%E5%AD%97full_scenario%E6%A8%A1%E5%BC%8F
preset_mode = "normal"

# 群内响应规则
# 符合此消息的群内消息即使不包含at机器人也会响应
# 支持消息前缀匹配及正则表达式匹配
# 支持设置是否响应at消息、随机响应概率
# 注意：由消息前缀(prefix)匹配的消息中将会删除此前缀，正则表达式(regexp)匹配的消息不会删除匹配的部分
#      前缀匹配优先级高于正则表达式匹配
# 正则表达式简明教程：https://www.runoob.com/regexp/regexp-tutorial.html
response_rules = {
    "at": True,  # 是否响应at机器人的消息
    "prefix": ["/ai", "!ai", "！ai", "ai"],
    "regexp": [],  # "为什么.*", "怎么?样.*", "怎么.*", "如何.*", "[Hh]ow to.*", "[Ww]hy not.*", "[Ww]hat is.*", ".*怎么办", ".*咋办"
    "random_rate": 0.0,  # 随机响应概率，0.0-1.0，0.0为不随机响应，1.0为响应所有消息, 仅在前几项判断不通过时生效
}

# 消息忽略规则
# 适用于私聊及群聊
# 符合此规则的消息将不会被响应
# 支持消息前缀匹配及正则表达式匹配
# 此设置优先级高于response_rules
# 用以过滤mirai等其他层级的指令
# @see https://github.com/RockChinQ/QChatGPT/issues/165
ignore_rules = {
    "prefix": ["/"],
    "regexp": []
}

# 是否检查收到的消息中是否包含敏感词
# 若收到的消息无法通过下方指定的敏感词检查策略，则发送提示信息
income_msg_check = False

# 敏感词过滤开关，以同样数量的*代替敏感词回复
# 请在sensitive.json中添加敏感词
sensitive_word_filter = True

# 是否启用百度云内容安全审核
# 注册方式查看 https://cloud.baidu.com/doc/ANTIPORN/s/Wkhu9d5iy
baidu_check = False

# 百度云API_KEY 24位英文数字字符串
baidu_api_key = ""

# 百度云SECRET_KEY 32位的英文数字字符串
baidu_secret_key = ""

# 不合规消息自定义返回
inappropriate_message_tips = "[百度云]请珍惜机器人，当前返回内容不合规"

# 启动时是否发送赞赏码
# 仅当使用量已经超过2048字时发送
encourage_sponsor_at_start = True

# 每次向OpenAI接口发送对话记录上下文的字符数
# 最大不超过(4096 - max_tokens)个字符，max_tokens为下方completion_api_params中的max_tokens
# 注意：较大的prompt_submit_length会导致OpenAI账户额度消耗更快
prompt_submit_length = 2048

# OpenAI补全API的参数
# 请在下方填写模型，程序自动选择接口
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
# 具体请查看OpenAI的文档: https://beta.openai.com/docs/api-reference/completions/create
# 请将内容修改到config.py中，请勿修改config-template.py
completion_api_params = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.9,  # 数值越低得到的回答越理性，取值范围[0, 1]
    "top_p": 1,  # 生成的文本的文本与要求的符合度, 取值范围[0, 1]
    "frequency_penalty": 0.2,
    "presence_penalty": 1.0,
}

# OpenAI的Image API的参数
# 具体请查看OpenAI的文档: https://beta.openai.com/docs/api-reference/images/create
image_api_params = {
    "size": "256x256",  # 图片尺寸，支持256x256, 512x512, 1024x1024
}

# 群内回复消息时是否引用原消息
quote_origin = True

# 回复绘图时是否包含图片描述
include_image_description = True

# 消息处理的超时时间，单位为秒
process_message_timeout = 30

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

# 消息处理出错时向用户发送的提示信息
# 仅当hide_exce_info_to_user为True时生效
# 设置为空字符串时，不发送提示信息
alter_tip_message = '出错了，请稍后再试'

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
rate_limit_strategy = "wait"

# drop策略时，超过限速均值时，丢弃的对话的提示信息
# 仅当rate_limitation_strategy为"drop"时生效
# 若设置为空字符串，则不发送提示信息
rate_limit_drop_tip = "本分钟对话次数超过限速次数，此对话被丢弃"

# 是否在启动时进行依赖库更新
upgrade_dependencies = True

# 是否上报统计信息
# 用于统计机器人的使用情况，不会收集任何用户信息
# 仅上报时间、字数使用量、绘图使用量，其他信息不会上报
report_usage = True

# 日志级别
logging_level = logging.INFO

# 定制帮助消息
help_message = """此机器人通过调用大型语言模型生成回复，不具有情感。
你可以用自然语言与其交流，回复的消息中[GPT]开头的为模型生成的语言，[bot]开头的为程序提示。
欢迎到github.com/RockChinQ/QChatGPT 给个star"""