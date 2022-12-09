
from cbr.plugin.info import MessageInfo
from cbr.plugin.cbrinterface import CBRInterface
import json
import os
import re
import random

#api
__all__ = [
    'get_qq_num',
    'get_player',
    'get_permission',
    'get_qq_num_dict',
    'get_permission_dict',
    'random_player',
    'check_player_name'
]

METADATA = {
    'id': 'qq_permission',
    'version': '0.1.4',
    'name': 'QQ_Permission',
    'description': 'add cqhttp client permission function to CBR',
    'author': 'Kongtu_Si',
    'link': 'https://github.com/Kongtu5i'
}

CONFIG_PATH = './config/qq_permission/config.json'
PERMISSION_PATH = './config/qq_permission/permission.json'
QQ_NUM_PATH = './config/qq_permission/qq_num.json'
DEFAULT_CONFIG = {
    "command_prefix": "##permission",
    "cqhttp_client_name": "cqhttp",
    "permission_level": 3
}
PERMISSION_LEVEL_LIST = [1, 2, 3, 4]

#传入qq号或者玩家名，返回值统一为玩家名
def sync_player(a: str) -> list:
    qq_num_dict = get_qq_num_dict()
    if a in qq_num_dict.keys():
        b = []
        b.append(a)
        return b
    elif a in qq_num_dict.values():
        return get_player(a) 
    return None

#文件路径是否存在
def is_path_exists(path: str) -> bool:
    if os.path.exists(path):
        return True
    else:
        return False

#读取json文件
def json_read(path: str) -> dict:
    with open(path, "r", encoding = "utf-8") as f:
        json_list = json.load(f)
    return json_list

#写入json文件
def json_dump(path: str, default_list: list) -> None:
    with open(path, "w", encoding = "utf-8") as f:
        json.dump(default_list, f, indent=4, ensure_ascii = False)

#获取发送消息者的qq号
def get_qq_user_id(server, info) -> str:
    '''
    获取发送消息者的qq号
    '''
    if server.is_mc_client(info.source_client):
        qq_user_id = get_qq_num(info.sender)
        return qq_user_id
    elif info.source_client == CQHTTP_CLIENT:
        qq_user_id = info.sender.split('_qq_user_id_', 1)[0]
        return qq_user_id
    return None

#检查玩家名是否正确(增加特定字符跳过检查功能)
def check_player_name_j(name :str) -> bool:
    '''
    这是我给增加的一个特殊功能的函数，特定字符结尾可以跳过玩家名检查，直接设置为true
    防止一些不必要的安全问题，所以我没有放进api里，其他用户请谨慎添加进api并使用
    如果使用这个函数，记得自己删掉玩家名的后缀
    '''
    if check_player_name(name):
        return True
    elif name.endswith('^jump_check'):#特定跳过字可以改，看你改不改:(:
        return True
    else:
        return False

#检查玩家名是否正确
def check_player_name(name: str) -> bool:
    '''
    玩家名命名格式无误返回True，否则返回False
    此函数代码来自HuajiMUR233
    项目地址:https://github.com/HuajiMURsMC/MCUUID
    '''
    if (re.fullmatch(r"\w+",name) is not None) and len(name)<=16 and not(name.lower().startswith('bot_')):
        return True
    else:
        return False

#获取完整qq号列表
def get_qq_num_dict() -> dict:
    '''
    返回值为玩家列表(dict)
    '''
    return json_read(QQ_NUM_PATH)

#获取完整权限列表
def get_permission_dict() -> dict:
    '''
    返回值为权限列表(dict)
    '''
    return json_read(PERMISSION_PATH)

#随机获取玩家名
def random_player() -> str:
    '''
    返回值为玩家名(str)
    '''
    qq_num_dict = json_read(QQ_NUM_PATH)
    return random.choice(list(qq_num_dict.keys()))

#通过玩家名获取qq号
def get_qq_num(player: str) -> str:
    '''
    返回值为qq号(str)
    如果玩家不存在，则返回 None
    '''
    qq_num_dict = json_read(QQ_NUM_PATH)
    if player in qq_num_dict.keys():
       return qq_num_dict[player]
    else:
        return None

#通过qq号获取玩家名(一个qq号可能绑定多个玩家,所以返回值为list)
def get_player(qq_num: str)-> list:
    '''
    返回值为玩家名(list)
    如果qq号不存在，则返回 None
    '''
    qq_num_dict = json_read(QQ_NUM_PATH)
    if not qq_num in qq_num_dict.values():
        return None
    else:
        player_list = []
        for i in qq_num_dict.keys():
            if qq_num_dict[i] == qq_num:
                player_list.append(i)
        return player_list

#获取对应qq号权限等级(默认权限等级为2)
def get_permission(qq_num: str)-> int:
    '''
    返回值为权限等级(int)
    如果qq号不存在，则返回默认权限等级1
    '''
    permission_dict = json_read(PERMISSION_PATH)
    if qq_num in permission_dict.keys():
        return permission_dict[qq_num]
    else:
        return 2

#发送消息
def send_message(server, info, msg: str) -> None:
    server.send_custom_message('', info.source_client, msg, '', info.sender)

#设置玩家权限
def set_permission(server, info):
    msg = info.content.replace(f'{PREFIX} set ', '')
    player_list = sync_player(msg.split(' ', 1)[0])
    if player_list == None:
        send_message(server, info, '§4玩家不存在')
        return
    try:
        permission_level = int(msg.split(' ', 1)[1])
        if not permission_level in PERMISSION_LEVEL_LIST:        
            send_message(server, info, '§4输入的权限等级有误')
            return
    except:
        send_message(server, info, '§4输入的权限等级有误')
        return
    sender_qq_num = get_qq_user_id(server, info)
    if sender_qq_num == None:
        send_message(server, info, '§4获取发送者QQ号失败')
        return
    if get_permission(sender_qq_num) < PERMISSION_LEVEL or get_permission(sender_qq_num) < permission_level:
        send_message(server, info, '§4权限不足')
        return
    permission_dict = get_permission_dict()
    player_qq_num = get_qq_num(player_list[0])
    a = ''
    for i in player_list:
        permission_dict[get_qq_num(i)] = permission_level
        a = a + ', ' + i
    send_message(server, info, f'§f设置玩家§6{a[2:]}§f的权限等级为: §a{permission_level}  §f(绑定的QQ号为: §a{player_qq_num}§f)')
    json_dump(PERMISSION_PATH, permission_dict)

#查询玩家信息
def query_permission(server, info):
    player_list = sync_player(info.content.replace(f'{PREFIX} query ', ''))
    if player_list == None:
        send_message(server, info, '§4玩家不存在')
        return
    player_qq_num = get_qq_num(player_list[0])
    permission_level = get_permission(player_qq_num)
    a = ''
    for i in player_list:
        a = a + ', ' + i
    msg = f'§f玩家§6{a[2:]}§f绑定的QQ号为: §a{player_qq_num}'
    msg = msg + '\n' + f'§f权限等级为: §a{permission_level}'
    send_message(server, info, msg)

#绑定玩家
#这辈子不想再看见这个函数了，逻辑好他妈的恶心
def bind_player(server, info):
    msg = info.content.replace(f'{PREFIX} bind ', '')
    player = msg.split(' ', 1)[0]
    if not check_player_name(player):
        send_message(server, info, '§4输入的玩家名有误')
        return
    player = player.split('^jump_check')[0]
    try:
        bind_qq_num = str(int(msg.split(' ', 1)[1]))
    except:
        send_message(server, info, '§4输入QQ号有误')
        return
    sender_qq_num = get_qq_user_id(server, info)
    if sender_qq_num == None:
        send_message(server, info, '§4获取发送者QQ号失败')
        return
    qq_num_dict = get_qq_num_dict()
    if sender_qq_num == bind_qq_num:#发送者qq号等于要绑定的qq号
        if get_qq_num(player) == None:#player在qq_num.json中不存在
            if get_player(sender_qq_num) == None:#发送者的qq号未绑定玩家
                qq_num_dict[player] = bind_qq_num
                json_dump(QQ_NUM_PATH, qq_num_dict)
                send_message(server, info, f'§f绑定玩家§6{player}§f至QQ号: §a{bind_qq_num}')
            #发送者的qq号已经绑定玩家
            elif get_permission(sender_qq_num) >= PERMISSION_LEVEL:#有权限
                qq_num_dict[player] = bind_qq_num
                json_dump(QQ_NUM_PATH, qq_num_dict)
                send_message(server, info, f'§f增加绑定玩家§6{player}§f至QQ号: §a{bind_qq_num}')
            else:#无权限
                send_message(server, info, f'§4一个QQ号顶多绑定一个玩家，如果要增加绑定玩家，请联系管理员')
        #player在qq_num.json中存在, 而且player对应的qq号和要绑定的qq号相同
        elif get_qq_num(player) == bind_qq_num:
            send_message(server, info, f'§f玩家§6{player}§f已绑定至QQ号: §a{bind_qq_num}')
        #player在qq_num.json中存在, 而且player对应的qq号和要绑定的qq号不相同
        elif get_permission(sender_qq_num) >= PERMISSION_LEVEL:#有权限
            qq_num_dict[player] = bind_qq_num
            json_dump(QQ_NUM_PATH, qq_num_dict)
            send_message(server, info, f'§f换绑玩家§6{player}§f至QQ号: §a{bind_qq_num}')
        else:#无权限
            send_message(server, info, f'§4权限不足, 无法换绑')
    #发送者qq号不等于要绑定的qq号
    elif get_permission(sender_qq_num) >= PERMISSION_LEVEL:#有权限
        if get_qq_num(player) == None:#player在qq_num.json中不存在
            if get_player(bind_qq_num) == None:#要绑定的qq号未绑定玩家
                qq_num_dict[player] = bind_qq_num
                json_dump(QQ_NUM_PATH, qq_num_dict)
                send_message(server, info, f'§f绑定玩家§6{player}§f至QQ号: §a{bind_qq_num}')
            else:#要绑定的qq号已绑定玩家
                qq_num_dict[player] = bind_qq_num
                json_dump(QQ_NUM_PATH, qq_num_dict)
                send_message(server, info, f'§f增加绑定玩家§6{player}§f至QQ号: §a{bind_qq_num}')
        else:
            #player在qq_num.json中存在
            qq_num_dict[player] = bind_qq_num
            json_dump(QQ_NUM_PATH, qq_num_dict)
            send_message(server, info, f'§f换绑玩家§6{player}§f至QQ号: §a{bind_qq_num}')
    else:
        send_message(server, info, f'§4权限不足')

#删除玩家信息
def del_player(server, info):
    sender_qq_num = get_qq_user_id(server, info)
    if sender_qq_num == None:
        send_message(server, info, '§4获取发送者QQ号失败')
        return
    if get_permission(sender_qq_num) < PERMISSION_LEVEL:
        send_message(server, info, '§4权限不足')
        return
    player_list = sync_player(info.content.replace(f'{PREFIX} del ', ''))
    if player_list == None:
        send_message(server, info, '§4玩家不存在')
        return
    qq_num_dict = get_qq_num_dict()
    player_qq_num = get_qq_num(player_list[0])
    a = ''
    for i in player_list:
        if i in qq_num_dict.keys():
            qq_num_dict.pop(i)
        a = a + ', ' + i
    if  player_qq_num in qq_num_dict.values():
        json_dump(QQ_NUM_PATH, qq_num_dict)
        send_message(server, info, f'§f已经删除玩家§6{a[2:]}§f的绑定信息')
    else:
        permission_dict = get_permission_dict()
        if player_qq_num in permission_dict.keys():
            permission_dict.pop(player_qq_num)
            json_dump(PERMISSION_PATH, permission_dict)
        json_dump(QQ_NUM_PATH, qq_num_dict)
        send_message(server, info, f'§f已经删除玩家§6{a[1:]}§f的所有信息(绑定的QQ号为: §a{player_qq_num}§f)')
        
#功能分流
def which_function(server, info):
    if not info.is_player():
        return
    if info.content == PREFIX:
        help_msg = f'''§f========================
§f使用 §6{PREFIX}§f 呼出帮助信息
§f指令形式为:
§f{PREFIX} set §6<玩家名/QQ号> §6<权限等级> §f设置玩家的权限等级
§f{PREFIX} query §6<玩家名/QQ号> §f查询玩家的相关信息
§f{PREFIX} bind §6<玩家名> §6<QQ号> §f绑定玩家至QQ号
§f{PREFIX} del §6<玩家名/QQ号> §f删除玩家的所有信息
§f使用示例:
§a{PREFIX} set can_yi_ 1
§f========================'''
        send_message(server, info, help_msg)
        return
    if info.content.startswith(f'{PREFIX} '):
        msg = info.content.replace(f'{PREFIX} ', '')
        if msg.startswith('set '):
            set_permission(server, info)
        if msg.startswith('query '):
            query_permission(server, info)
        if msg.startswith('bind '):
            bind_player(server, info)
        if msg.startswith('del '):
            del_player(server, info)

def on_message(server: CBRInterface, info: MessageInfo):
    which_function(server, info)

def on_command(server, info):
    which_function(server, info)

def on_load(server):
    global PREFIX
    global CQHTTP_CLIENT
    global PERMISSION_LEVEL
    if not is_path_exists('./config/qq_permission'):
        os.mkdir('./config/qq_permission')
    if not is_path_exists(CONFIG_PATH):
        json_dump(CONFIG_PATH, DEFAULT_CONFIG)
    if not is_path_exists(PERMISSION_PATH):
        json_dump(PERMISSION_PATH, {'3264868705': 3})
    if not is_path_exists(QQ_NUM_PATH):
        json_dump(QQ_NUM_PATH, {'Kongtu_Si': '3264868705'})
    config_list = json_read(CONFIG_PATH)
    PREFIX = config_list['command_prefix']
    CQHTTP_CLIENT = config_list['cqhttp_client_name']
    PERMISSION_LEVEL = config_list['permission_level']
