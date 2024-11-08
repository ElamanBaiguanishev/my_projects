import asyncio
import datetime
import random
import time

from aiohttp import ClientSession

loos = []

with open('proxy.txt') as file:
    proxies = file.read().splitlines()


async def check_validate_requests_async(url, proxy_dict=None, timeout=40):
    try:
        async with ClientSession() as session:
            response = await session.get(url, proxy=proxy_dict, timeout=timeout)
            if "robots" in await response.text():
                print(f"False {url} {proxy_dict}")
                return False
            print(f"True {url} {proxy_dict}")
            return True
    except Exception as e:
        loos.append(proxy_dict)
        prox = list(set(proxies) - set(loos))
        await check_validate_requests_async(url, f'http://{random.choice(prox)}', 20)


arr = [f'https://t.me/user{i}' for i in range(1000)]


async def main():
    tasks = [check_validate_requests_async(url, f'http://{proxies[i % len(proxies)]}') for i, url in
             enumerate(arr)]
    await asyncio.gather(*tasks)


time_start = datetime.datetime.now()
if __name__ == "__main__":
    asyncio.run(main())
time.sleep(10)
time_end = datetime.datetime.now()
print((time_end - time_start).total_seconds())
