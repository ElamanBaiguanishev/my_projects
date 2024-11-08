import asyncio
import random
import aiohttp


# async def check_validate_requests_async(session, url, proxy_dict=None):
#     try:
#         async with session.get(url, proxy=proxy_dict) as response:
#             if response.status == 200:
#                 page_content = await response.text()
#                 if "tgme_page_icon" in page_content:
#                     print(f"False {url} {proxy_dict}")
#                     return False
#             print(f"True {url} {proxy_dict}")
#             return True
#     except:
#         await check_validate_requests_async(session, url, f'http://{random.choice(proxies)}')
