import asyncio
import aiohttp
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
resultList = []


class Spider(object):
    def __init__(self, end, url, score):
        # 设置最大信号量
        self.semaphore = asyncio.Semaphore(6)
        # 伪装请求头
        self.header = {
            "Host": "club.jd.com",
            "Cookie": "shshshfpa=c003ed54-a640-d73d-ba32-67b4db85fd3e-1594895561; shshshfpb=i5%20TzLvWAV56AeaK%20C9q5ew%3D%3D; __jdu=629096461; unpl=V2_ZzNtbUVRFkZ8DUddfRxcBGIEE1hKXhBGIQEVVnNLD1IwBkBeclRCFnQUR1JnGloUZwEZXkZcQxVFCEdkeR1ZAmYBEV1yZ0IXJQ4SXS9NVAZiChAJQAdGFnJfRFQrGlUAMFdACUtVcxZ1OEdkfBpUBG8EF1pCZ3MVfQ92ZDBMAGshQlBtQldEEXAKTlZyGGwEVwMTWUFXQxZ1DkFkMHddSGAAGlxKUEYSdThGVXoYXQVkBBVeclQ%3d; __jdv=122270672|baidu|-|organic|not set|1596847892017; areaId=0; ipLoc-djd=1-72-55653-0; PCSYCityID=CN_0_0_0; __jda=122270672.629096461.1595821561.1596847892.1597148792.3; __jdc=122270672; shshshfp=4866c0c0f31ebd5547336a334ca1ef1d; 3AB9D23F7A4B3C9B=DNFMQBTRNFJAYXVX2JODGAGXZBU3L2TIVL3I36BT56BKFQR3CNHE5ZTVA76S56HSJ2TX62VY7ZJ2TPKNIEQOE7RUGY; jwotest_product=99; shshshsID=ba4014acbd1aea969254534eef9cf0cc_5_1597149339335; __jdb=122270672.5.629096461|3.1597148792; JSESSIONID=99A8EA65B8D93A7F7E8DAEE494D345BE.s1",
            "Connection": "keep-alive",
            "Referer": "https://item.jd.com/4803334.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"

        }
        self.end = end  # 要爬取的评论页数目
        self.id = url[20:-5]
        self.score = score

    async def scrape(self, url):
        async with self.semaphore:
            session = aiohttp.ClientSession(headers=self.header)
            response = await session.get(url)
            result = await response.text()
            await session.close()
            return result

    async def scrape_page(self, page):
        # 分别手动改变score参数 score=3 score=2 score=1  爬取好评 中评 差评数据
        url = f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={self.id}&score={self.score}&sortType=6&page={page}&pageSize=10&isShadowSku=0&fold=1'
        text = await self.scrape(url)
        await self.parse(text)

    async def parse(self, text):
        global resultList
        # 正则匹配提取数据
        content = re.findall('"guid":".*?","content":"(.*?)"', text)
        # 保存到txt
        for con in content:
            resultList.append(con)

    def main(self):
        # 爬取100页的数据
        scrape_index_tasks = [asyncio.ensure_future(self.scrape_page(page)) for page in range(0, self.end)]
        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(*scrape_index_tasks)
        loop.run_until_complete(tasks)


def getList(page, url, score):
    spider = Spider(page, url, score)
    spider.main()
    return resultList
# https://item.jd.com/7874705.html