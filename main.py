"""用户输入 /News 获取60秒读懂世界图片"""
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import aiohttp
import asyncio

# 接口地址
API_URL = "https://v.api.aa1.cn/api/60s-v3/"

@register("今日新闻", "egg", "60秒国内新闻", "1.0.0", "https://github.com/bbpn-cn/headline")
class NewsPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def verify_image(self, session):
        """验证接口是否返回图片"""
        try:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if isinstance(content_type, bytes):
                        content_type = content_type.decode('utf-8')
                    if content_type.startswith('image/'):
                        return True
                return False
        except aiohttp.ClientError:
            return False

    @filter.command("News")
    async def news_command(self, event: AstrMessageEvent):
        '''新闻查询指令，使用格式：/News'''
        yield event.plain_result("正在获取今日新闻...")

        async with aiohttp.ClientSession() as session:
            if await self.verify_image(session):
                yield event.image_result(API_URL)  # 直接传入 URL
            else:
                yield event.plain_result("无法获取今日新闻，请稍后再试。")

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
