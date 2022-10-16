import re
from mcdreforged.api.all import *
from uuid_api import *


def on_load(server: PluginServerInterface, old):
    server.register_help_message("!!petmove", "give your nearest pet to someone else online")    #注册!!help信息

    server.register_command(Literal('!!petmove')
    .then(Text('playerName')))       #注册!!petmove命令

def on_user_info(server: ServerInterface, info: Info):
    if info.content.startswith("!!petmove "):
        args = info.content.split(" ")

        if (len(args) != 2):
            server.tell(info.player, '[petmove] !!petmove <playerName>')
            return
        
        playername = args[1]
        targetUUID = get_UUID_by_playername(playername)     #获取目标玩家UUID
        #修改主人
        server.execute(
            'execute as ' + info.player + ' at ' + info.player + ' run data modify entity @e[type=!minecraft:player,sort=nearest,limit=1] Owner set value "' + targetUUID + '"')    #修改
        server.execute(
            'execute as ' + playername + ' at ' + playername + ' run effect give @e[type=!minecraft:player,sort=nearest,limit=1] glowing')  #高亮
    
    elif info.content == '!!petmove':
        server.tell(info.player, '[petmove] give your nearest pet to someone else online')

def get_UUID_by_playername(playername):
    playerUUID = get_uuid(playername)

    playerUUID = playerUUID[0:8] + '-' + playerUUID[8:12] + '-' + playerUUID[12:16] + '-' + playerUUID[16:20] + '-' + playerUUID[20:32]
    return playerUUID