# qq_permission插件  
为CBR添加权限功能，权限控制在MC客户端和cqhttp客户端都可以控制  
同时，qq_permission提供了一些api，可以供其他插件开发者使用，详细信息请下翻  
注意：请下载我主页的CBR项目中的ChatBridgeReforged_cqhttp.py作为cqhttp客户端来使用  
小声嘀咕：也可以使用我的ChatBridgeReforged_MC.py作为MC客户端，在ricky的MC客户端基础上增加了一点新功能  
另外，非常重要：最开始使用时，需要手动绑定群内所有玩家的qq号

## 使用方法  
配置文件里的command_prefix为命令前缀，可以自行修改  
cqhttp_client_name为你cqhttp客户端的名字  
permission_level是进行权限操作需要的权限等级  
权限等级为1、2、3、4，其中4为最高，1为最低，默认权限等级2，类似MCDR的权限等级

使用##permission呼出帮助（默认是这个，根据你配置文件里的command_prefix来的）  
##permission set <玩家名/QQ号> <权限等级> 设置玩家的权限等级  
##permission query <玩家名/QQ号> 查询玩家的相关信息  
##permission bind <玩家名> <QQ号> 绑定玩家至QQ号  
##permission del <玩家名/QQ号> 删除玩家的所有信息  

## api(仅面向开发者用户)  
### check_player_name(name: str)->bool  
检查玩家名是否符合规范，并没有访问mojang服务器检查，所以请谨慎使用  
玩家名符合规范返回 True，否则为 False  
### get_qq_num_dict()->dict  
返回完整的玩家列表，即qq_num.json中的全部信息  
### get_permission_dict()->dict  
返回完整的权限列表，即permission.json中的全部信息  
### random_player()->str  
随机获得一个玩家的名字，emmmm我也不知道能干啥，随机删除一个玩家的白名单？  
### get_qq_num(player: str)->str  
获得对应玩家的qq号  
返回值为qq号(str)，如果玩家不存在，则返回 None  
### get_player(qq_num: str)->list  
获得qq号所绑定的玩家  
返回值为玩家名(list)，如果qq号不存在，则返回 None  
一个玩家可能有多个MC账号，所以返回值为list  
### get_permission(qq_num: str)->int
获取对应qq号的权限等级  
返回值为权限等级(int)，如果qq号不存在，则返回默认权限等级1  
