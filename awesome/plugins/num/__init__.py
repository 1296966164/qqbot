from awesome.plugins.num.number import search
from nonebot import on_command, CommandSession
# on_command 装饰器将函数声明为一个命令处理器
# 这里为命令的名字，同时允许使用别名


__plugin_name__ = '查学号'
__plugin_usage__ = r'''
xh 姓名
'''


@on_command('xh', aliases=('学号','查学号'))
async def xh(session: CommandSession):
    # 从会话状态（session.state）中获取name，如果当前不存在，则询问用户
    name = session.get('name', prompt='你想查找谁呢？')
    # 查询
    info = search(name)
    # 向用户发送结果
    await session.send(info)


# weather.args_parser 装饰器将函数声明为 xh 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@xh.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符

    stripped_arg = session.current_arg_text.strip()
    print(stripped_arg)

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        print(1111111111111111111111111111)
        print(stripped_arg, "000000000000000000")

        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['name'] = stripped_arg
        return


    if not session.is_first_run:
        print(2222222222222222222222222222)
        print(stripped_arg)

        if not stripped_arg:
            # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
            # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
            session.pause('要查询的姓名不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
    print(stripped_arg)


