#满血版的色图插件

import time
import requests
from cbr.plugin.info import MessageInfo
from cbr.plugin.cbrinterface import CBRInterface

CLIENT = "cqhttp"

METADATA = {
    'id': 'setu-plus',
    'version': '0.3.0',
    'name': 'SeTu-Plus',
    'description': '',
    'author': 'Kongtu_Si',
    'link': ''
}

split_str = '"urls":{"regular":"'
image1 = "[CQ:image,file="
image2 = ",c=3,subType=0]"
api_url = "https://api.lolicon.app/setu/v2?size=regular"

#get setu
def get_setu(url):
    image = ""
    try:
        setu_dirt = requests.get(url, timeout=10).text
        setu_url = setu_dirt.split(split_str)[1].split('"')[0]
        image = image1 + setu_url + image2
        return image
    except:
        #print("some error!")
        return None

#is str is a num
def is_num(str):
    try:
        float(str)
        return True
    except:
        return False

#main function
def setu(server, info):
    if info.content.startswith("#setu") or info.content.startswith("#色图"):
        if info.source_client != CLIENT:
            server.reply(info, "哟，还敢要色图？我发了你能用MC看吗？笨比（")
            return
        msg = info.content.replace("#setu", "").replace("#色图", "")
        if msg == "" or msg == " ":
            image = get_setu(api_url)
            server.reply(info, "注意身体！")
            if image != None:
                server.reply(info, image)
        else:
            msg_list = msg.split(" ")
            if len(msg_list) == 2:
                if is_num(msg_list[1]):
                    if float(msg_list[1]) < 1 or float(msg_list[1]) > 5 or float(msg_list[1]) - int(float(msg_list[1])) != 0:
                        server.reply(info, "输入的图片数量有误！")
                    else:
                        #print(msg_list[1])
                        num = int(msg_list[1])
                        server.reply(info, "注意身体！")
                        while num != 0:
                            image = get_setu(api_url)
                            if image != None:
                                server.reply(info, image)
                            num = num - 1
                            time.sleep(0.5)
                else:
                    url = api_url + "&tag=" + msg_list[1]
                    #print(url)
                    image = get_setu(url)
                    server.reply(info, "注意身体！")
                    if image != None:
                        server.reply(info, image)
            else:
                if len(msg_list) == 3:
                    if is_num(msg_list[2]):
                        if int(msg_list[2]) < 1 or int(msg_list[2]) > 5 or float(msg_list[2]) - int(float(msg_list[2])) != 0:
                            server.reply(info, "输入的图片数量有误！")
                        else:
                            url = api_url + "&tag=" + msg_list[1]
                            #print(url)
                            num = int(msg_list[2])
                            server.reply(info, "注意身体！")
                            while num != 0:
                                image = get_setu(url)
                                if image != None:
                                    server.reply(info, image)
                                num = num - 1
                                time.sleep(0.5)
                    else:
                        server.reply(info, "输入的图片数量有误！")

def on_message(server: CBRInterface, info: MessageInfo):
    setu(server, info)

def on_command(server, info): 
    setu(server, info)