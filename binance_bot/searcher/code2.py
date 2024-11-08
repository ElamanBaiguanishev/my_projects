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
                return f"{url_}: ➖,"  # Формируем строку для невалидного URL
    return f"{url_}: ➕,"


async def validate_urls():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(10)  # Ограничение на количество одновременных запросов
        tasks = []
        for i in data_:
            task = check_validate(session, semaphore, i)
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        invalid_urls_str = "".join(results)  # Объединяем результаты в строку
        print(invalid_urls_str)
        print(len(invalid_urls_str))


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(validate_urls())
    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
