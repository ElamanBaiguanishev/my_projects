import requests


def check_validate(url_: str):
    response = requests.get(url_)
    if response.status_code == 200:
        page_content = response.text
        if "tgme_page_icon" in page_content:
            return False
    return True
