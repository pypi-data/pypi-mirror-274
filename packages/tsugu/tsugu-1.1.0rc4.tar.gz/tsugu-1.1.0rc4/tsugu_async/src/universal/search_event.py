from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, MultiVar


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["查活动"],
        Args["word#请输入活动名，乐队，活动ID等查询参数", MultiVar(str)],
        meta=CommandMeta(
            compact=config.compact, description="查活动",
            usage='根据关键词或活动ID查询活动信息',
            example='''查活动 绿 tsugu :返回所有属性加成为pure，且活动加成角色中包括羽泽鸫的活动列表
查活动 177 :返回177号活动的信息
查活动 >225 :查询大于225的活动
查活动 220-225 :查询220到225的活动'''
        )
    ).parse(message)

    if res.matched:
        return await tsugu_api_async.search_event(user.default_server, " ".join(res.word))

    return res

