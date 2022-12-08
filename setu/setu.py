#阉割版的色图插件


import requests
from cbr.plugin.info import MessageInfo
from cbr.plugin.cbrinterface import CBRInterface


CLIENT = "QQ"


METADATA = {
    'id': 'setu',
    'version': '0.3.0',
    'name': 'SeTu',
    'description': '',
    'author': 'Kongtu_Si',
    'link': ''
}


split_str = '"urls":{"regular":"'
image1 = "[CQ:image,file="
image2 = ",c=3,subType=0]"
api_url = "https://api.lolicon.app/setu/v2?size=regular"


def get_setu(url):
    image = ""
    try:
        setu_dirt = requests.get(url, timeout=10).text
        setu_url = setu_dirt.split(split_str)[1].split('"')[0]
        image = image1 + setu_url + image2
        return image
    except:
        return None


def setu(server, info):
    if info.content == "#setu" or info.content == "#色图":
        if info.source_client != CLIENT:
            server.reply(info, "哟，还敢要色图？我发了你能用MC看吗？笨比（")
            return
        image = get_setu(api_url)
        server.reply(info, "注意身体！")
        if image != None:
            server.reply(info, image)



def on_message(server: CBRInterface, info: MessageInfo):
    setu(server, info)


def on_command(server, info): 
    setu(server, info)
