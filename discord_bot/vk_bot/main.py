import re

from vk_api import vk_api
from vkbottle.bot import Bot, Message

bot = Bot("81bea9a533ee468fd9ec03365deaf39c53370802d7fc4cac960d8f75bef4fbc5dbdc65d82a0b49daed084")

vk_session = vk_api.VkApi(
    token='vk1.a.48NPrA5XfyjbampV6fiEZF5kPKDu3CUVIBuICdA_tvHcFETa4je5Db82u3pot25ndb7Do5Vybho7UfsNsuwCFrMiJb9zAg4ntP4QKB6DIvZcBdzj3CAGh4vVDDd0mcvo2H-irQjmfdwoiCTVgQ2TNA9VXxaiVc7_0YPw4lmV1eRKyGkL5zlAQZlZI7jXCOTNhRQbvhiFj3QU1DJKaxR1Kg')  # подключаемся к VK API с помощью токена пользователя
vk = vk_session.get_api()


def get_id(url):
    match = re.search(r'vk.com/(\w+)', url)
    if match:
        user_id = match.group(1)
        return user_id  # Выводит 'pavelkurtzz'
    else:
        return url


@bot.on.message(text="!<url>")
async def any_message(message: Message, url):
    user_info = vk.users.get(user_ids=get_id(url), fields='photo_max')[0]

    avatar_link = user_info['photo_max']  # забираем ссылку на аватарку из полученной информации

    await message.answer(avatar_link)


bot.run_forever()
