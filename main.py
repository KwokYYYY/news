"""用户输入 /今日新闻 获取60秒读懂世界图片"""
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import aiohttp
import asyncio

# 接口地址
API_URL = "https://v.api.aa1.cn/api/60s-v3/"

@register("今日新闻", "Your Name", "获取60秒读懂世界图片的插件", "1.0.0", "repo url")
class NewsPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def fetch_image(self, session):
        """从接口获取图片数据"""
        try:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    # 获取 Content-Type 并确保是字符串
                    content_type = response.headers.get('Content-Type', '')
                    if isinstance(content_type, bytes):
                        content_type = content_type.decode('utf-8')  # 转换为字符串
                    if content_type.startswith('image/'):
                        return await response.read()
                    else:
                        return None
                return None
        except aiohttp.ClientError:
            return None

    @filter.command("今日新闻")
    async def news_command(self, event: AstrMessageEvent):
        '''新闻查询指令，使用格式：/今日新闻'''
        yield event.plain_result("正在获取今日新闻图片...")

        async with aiohttp.ClientSession() as session:
            image_data = await self.fetch_image(session)
            if image_data:
                yield event.image_result(image_data)  # 只传入图片数据
            else:
                yield event.plain_result("无法获取今日新闻图片，请稍后再试。")

    async def terminate(self):
        '''插件卸载时调用'''
        pass

if __name__ == "__main__":
    # 本地测试代码（不依赖 AstrBot）
    async def test():
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    data = await response.read()
                    print("图片数据获取成功，长度:", len(data))
                else:
                    print("获取失败，状态码:", response.status)

    asyncio.run(test())