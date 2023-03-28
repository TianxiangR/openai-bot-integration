from nonebot import get_driver
from .config import Config
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import EventMessage
from nonebot.plugin import on_command, on_message
from nonebot.log import logger
from plugins.chatgpt.util import EventUserId
from .util import EventUserId
from .chatgptAdapter import ChatGPTAdapter
import nonebot
from nonebot.adapters.onebot import V11Adapter

super_users = ['644120622']
WARNING_NOT_SUPER_USER = "您不是Super User，无法使用指令哦！"

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)

nonebot.load_plugin('nonebot_plugin_gocqhttp')
global_config = get_driver().config
config = Config.parse_obj(global_config)

chatgptAdapter = ChatGPTAdapter()
chatGPT = on_message(to_me())
reset_command = on_command('reset')
start_command = on_command('init')
terminate_command = on_command('terminate')
pause_command = on_command('pause')
continue_command = on_command('continue')
search_on_command = on_command('search_on')
search_off_command = on_command('search_off')

on_flag = True
search_flag = False


def isSuperUser(user_id: str) -> bool:
    global super_users
    return user_id in super_users


@chatGPT.handle()
async def handle(message: Message = EventMessage(), user_id: str = EventUserId()):
    if on_flag:
        user_message = message.extract_plain_text()
        if user_message is not None:
            if len(user_message) > 0 and user_message[0] == '/':
                return

            response = chatgptAdapter.getResponse(user_message, user_id)
            await chatGPT.send(Message(response))


@reset_command.handle()
async def on_reset(user_id: str = EventUserId()):
    if isSuperUser(user_id):
        chatgptAdapter.reset()
        await reset_command.send(Message("重置成功！"))
    else:
        await reset_command.send(Message(WARNING_NOT_SUPER_USER))


@start_command.handle()
async def on_start(user_id: str = EventUserId()):
    global on_flag
    if isSuperUser(user_id):
        if not on_flag:
            on_flag = True
            await start_command.send(Message("聊天机器人已启动"))
        else:
            await start_command.send(Message("聊天机器人已经在运行中"))
    else:
        await start_command.send(Message(WARNING_NOT_SUPER_USER))


@terminate_command.handle()
async def on_terminate(user_id: str = EventUserId()):
    global on_flag
    if isSuperUser(user_id):
        if on_flag:
            on_flag = False
            chatgptAdapter.reset()
            await start_command.send(Message("聊天机器人已关闭"))
        else:
            await start_command.send(Message("聊天机器人已出于关闭状态"))
    else:
        await start_command.send(Message(WARNING_NOT_SUPER_USER))


@pause_command.handle()
async def on_pause(user_id: str = EventUserId()):
    global on_flag
    if isSuperUser(user_id):
        if on_flag:
            on_flag = False
            await start_command.send(Message("聊天机器人已暂停服务"))
        else:
            await start_command.send(Message("聊天机器人已出于暂停状态"))
    else:
        await start_command.send(Message(WARNING_NOT_SUPER_USER))


@continue_command.handle()
async def on_continue(user_id: str = EventUserId()):
    global on_flag
    if isSuperUser(user_id):
        if not on_flag:
            on_flag = True
            await continue_command.send(Message("聊天机器人继续为您服务"))
        else:
            await continue_command.send(Message("聊天机器人已经在运行中"))
    else:
        await continue_command.send(Message(WARNING_NOT_SUPER_USER))


@search_on_command.handle()
async def turn_on_search(user_id: str = EventUserId()):
    if isSuperUser(user_id):
        chatgptAdapter.turnOnSearch()
        await search_on_command.send(Message("打开搜索模式...\n将失去连续对话能力\n该功能仍在实验中，可能会有不响应的情况"))
    else:
        await search_on_command.send(
            Message(WARNING_NOT_SUPER_USER))


@search_off_command.handle()
async def turn_off_search(user_id: str = EventUserId()):
    if isSuperUser(user_id):
        chatgptAdapter.turnOffSearch()
        await search_off_command.send(Message("关闭搜索模式...\n进入聊天模式"))
    else:
        await search_off_command.send(Message(WARNING_NOT_SUPER_USER))



