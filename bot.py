from pathlib import Path

import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter  # 避免重复命名


# 初始化 NoneBot
nonebot.init()

# 在这里加载插件
# nonebot.load_builtin_plugins("echo")  # 内置插件
# nonebot.load_builtin_plugin('echo')
nonebot.load_plugin(Path("./plugins/chatgpt"))
# nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
# nonebot.load_plugins("awesome_bot/plugins")  # 本地插件

if __name__ == "__main__":
    nonebot.run()