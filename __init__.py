import json
from mcdreforged.api.all import *


def on_load(server: PluginServerInterface, old):
    server.register_help_message("!!petmove", "give your nearest pet to someone else")    #注册!!help信息

    server.register_command(Literal('!!petmove')
    .then(Text('playerName')))       #注册!!petmove命令

def on_user_info(server: ServerInterface, info: Info):
    if info.content.startswith("!!petmove "):   #玩家输入判断
        args = info.content.split(" ")

        if (len(args) != 2):
            server.tell(info.player, '[petmove] !!petmove <playerName>')
            return
        
        playername = args[1]
        targetUUID = get_UUID_by_playername(server, info, playername)     #获取目标玩家UUID
        #修改主人
        server.execute(
            'execute as ' + info.player + ' at ' + info.player + ' run data modify entity @e[type=!minecraft:player,sort=nearest,limit=1] Owner set value "' + targetUUID + '"')    #修改
        server.execute(
            'execute as ' + playername + ' at ' + playername + ' run effect give @e[type=!minecraft:player,sort=nearest,limit=1] glowing')  #高亮
        server.logger.debug('petmove executor -> ' + info.player + ' to ' + playername + ' success')
    
    elif info.content == '!!petmove':
        server.tell(info.player, '[petmove] give your nearest pet to someone else')

def get_UUID_by_playername(server:ServerInterface, info:Info, playername:str):
    with open('./server/usercache.json', 'r') as usercache_fp:      #打开usercache.json读取uuid
        jsonAll = json.load(usercache_fp)                           #解析
        jsonObjectNum = len(jsonAll)                                #获取对象长度
        playerUUID = None

        for i in range(jsonObjectNum):
            if jsonAll[i]['name'] == playername:                    #检查玩家名字
                playerUUID = jsonAll[i]['uuid']
                return playerUUID

        if playerUUID == None:                                      #未检索到玩家名时
            server.tell(info.player, '[petmove] player named ' + playername + ' is not recorded by the server !')
            return