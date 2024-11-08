import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


# def check_validate_urllib(url_: str):
#     response = urlopen(url_)
#     if response.getcode() == 200:
#         page_content = response.read().decode('utf-8')
#         soup = BeautifulSoup(page_content, "html.parser")
#         icon_div = soup.find("div", class_="tgme_page_icon")
#         if icon_div:
#             return False
#     return True


def check_validate_requests(url_: str):
    response = requests.get(url_)
    if response.status_code == 200:
        page_content = response.text
        if "tgme_page_icon" in page_content:
            return False
    return True


# def validate_url_multiple_times(url: str, attempts: int):
#     results = []
#     for _ in range(attempts):
#         result = check_validate_urllib(url)
#         result1 = check_validate_requests(url)
#         results.append(result)
#         results.append(result1)
#
#     return all(results)


# for i in range(100):
#     print(validate_url_multiple_times("https://t.me/user68", 1))
