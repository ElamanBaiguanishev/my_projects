import asyncio
import time

import aiohttp

from searcher.db import get_data

data_: list = get_data(6098353259)


async def check_validate(session, url_: str):
    async with session.get(url_) as response:
        if response.status == 200:
            page_content = await response.text()
            if "tgme_page_icon" in page_content:
                return False
    return True


async def validate_urls():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in data_:
            tasks.append(check_validate(session, i))

        results = await asyncio.gather(*tasks)
        data = ""
        for i, result in enumerate(results):
            if not result:
                data = data + f"{data_[i]}: ➖"
        print(data)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(validate_urls())
    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
