'''
@author: lyx
@contact: woshiluyangxing@qq.com
@file: bilibili.py
@time: 2019-07-29 21:06
@desc:
'''

""" 获取B站番剧的今日更新
"""
import json

import requests
from nonebot import CommandSession, on_command


@on_command('bilibili', only_to_me=False)
async def bilibili_today(session: CommandSession):
    try:
        output = ''
        response = requests.get(
            'https://bangumi.bilibili.com/web_api/timeline_global')
        data = response.content.decode('utf-8')
        rjson = json.loads(data)
        for day in rjson['result']:
            if (day['is_today'] == 1):
                for item in day['seasons']:
                    output += f'{item["pub_time"]} : {item["title"]}  \n  [CQ:image,file={item["square_cover"]}]   \n'

        # 去掉最后一个\n
        await session.send(output[:-1])
    except:
        await session.send('获取番剧信息失败了~>_<~')
