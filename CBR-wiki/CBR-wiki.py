#from a same name MCDR-plugin
from cbr.plugin.info import MessageInfo
from cbr.plugin.cbrinterface import CBRInterface
from urllib.parse import quote

#触发指令，可自行更改，例如可改为：!!wiki     为了与CBR的控制指令保持一致，这里暂时用了##开头的触发指令
PREFIX = '##wiki'

PLUGIN_METADATA = {
    'id': 'CBR-wiki',
    'version': '1.0.0',
    'name': 'CBR-Wiki',
    'description': '快速在MCWiki查询你想要的东西(由MCDR插件移植)',
    'author': 'GamerNoTitle、Kongtu_Si',
    'link': 'https://github.com/GamerNoTitle/MCDR-WikiSearcher',
}

help_msg=f'''
§r======= §6Minecraft Wiki Searcher §r=======
§r帮助你更好地搜索Minecraft Wiki~
§r使用§6{PREFIX}§r可以叫出本使用方法
§r使用§6{PREFIX} [搜索内容]§r可以调用搜索
§r======= §6Minecraft Wiki Searcher §r=======
'''

def replace_msg(msg):
    msg = msg.replace(PREFIX, "")
    return msg

def wiki(server, info):
    if info.content.lower().startswith(PREFIX):
        info.cancel_send_message()
        msg = replace_msg(info.content.lower())
        if msg == "" or msg == " ":
            server.send_custom_message("§6wiki§7", info.source_client, help_msg, "", info.sender)
        else:
            tellraw_cmd = 'tellraw ' + info.sender + ' {"text":"§7[§6wiki§7]§r 在MCwiki中搜索 §a' + msg[1:] + '§r 的结果","underlined":"false","clickEvent":{"action":"open_url","value":"https://minecraft-zh.gamepedia.com/index.php?search=' + quote(msg[1:]) + '"}}'
            server.execute_command(info.source_client, tellraw_cmd)

def on_message(server: CBRInterface, info: MessageInfo):
    wiki(server, info)

def on_command(server, info):
    wiki(server, info)

def on_load(server: CBRInterface):
    server.register_help_message(f"{PREFIX}", "快速在MCWiki中查询")