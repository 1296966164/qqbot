'''
@author: lyx
@contact: woshiluyangxing@qq.com
@file: __init__.py.py
@time: 2020-01-14 15:34
@desc:
'''
from nonebot import CommandSession, on_command, get_bot, load_plugins
from nonebot.permission import *

from config import rootPath

__plugin_name__ = '遥控机器人 (private)'
__plugin_usage__ = r'''feature: 遥控
    发送消息：
    发送到群 [群号] [内容]
    发送到QQ [QQ号] [内容]
    查看已加入的群：
    所在的群
    重置已加载的插件：
    重置插件
'''


class ops:
    @staticmethod
    async def send_to_x(session: CommandSession, msg_type: str):
        bot = get_bot()
        param = session.get('param')
        paramSplit = param.split(' ', 1)
        targetId, toSend = paramSplit[0], paramSplit[1]

        try:
            if msg_type == 'group':
                await bot.send_group_msg(group_id=targetId, message=toSend)
            elif msg_type == 'private':
                await bot.send_private_msg(user_id=targetId, message=toSend)
            await session.send('success!')
        except CQHttpError as exc:
            await session.send(str(exc))

    @staticmethod
    async def arg_parser_x(session: CommandSession):
        argStripped = session.current_arg.strip()
        if argStripped:
            session.state['param'] = argStripped
        else:
            await session.send('用法：\n发送到群/QQ [群号/QQ] [内容]')
            session.finish()


@on_command('发送到群', permission=SUPERUSER, privileged=True)
async def send_to_group(session: CommandSession):
    await ops.send_to_x(session, 'group')


@on_command('发送到QQ', permission=SUPERUSER, privileged=True)
async def send_to_private(session: CommandSession):
    await ops.send_to_x(session, 'private')


@send_to_group.args_parser
@send_to_private.args_parser
async def group_arg_parse(session: CommandSession):
    await ops.arg_parser_x(session)


@on_command('所在的群', permission=SUPERUSER, privileged=True)
async def groups_in(session: CommandSession):
    groups: dict = await get_bot().get_group_list()
    res = ''
    for each in groups:
        res += f'{each["group_id"]}: {each["group_name"]}\n'
    res = res.rstrip('\n')
    await session.send(res)


@on_command('重置插件', permission=SUPERUSER, privileged=True)
async def reset_plugins(session: CommandSession):
    from os import path
    res=load_plugins(
        path.join(rootPath,'awesome','plugins'),
    'awesome.plugins')

    await session.send(res)