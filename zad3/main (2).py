from vkbottle import Bot, Message
import os
import random
import mc


bot=Bot('token') # Тут токен группы 
groupid = 187187101 # ид группы regvk.com/id/

# Важные переменные
meeting = '''Здарова, че я здесь забыл?
Ну раз пригласили, то не забудьте выдать мне доступ ко всей переписке в настройках беседы, а то НИЧЕГО не получится!

Список команд доступен по команде /help
F.A.Q - https://vk.com/@vitalik1338-faq
'''

dir_to_txt = 'Dialogs/dialogs'

async def check(ans, id: int) -> bool:
    items = (await bot.api.messages.get_conversations_by_id(peer_ids=ans.peer_id)).items
    if not items:
        return False
    chat_settings = items[0].chat_settings
    admins = []
    admins.extend(chat_settings.admin_ids)
    admins.append(chat_settings.owner_id)
    return id in admins

async def addtobd(peerid):
    if not os.path.exists(dir_to_txt + str(peerid) + '.txt'):
        f = open(dir_to_txt + str(peerid) + '.txt', 'w', encoding='utf8')
        f.write('')
        f.close()

@bot.on.chat_action("chat_invite_user", {"member_id": -groupid})
async def on_bot_invite(ans: Message):
    await addtobd(ans.peer_id)
    await ans(meeting)

@bot.on.chat_message(text=['/команды', '/help', 'команды', 'help', '/помощь', 'помощь'], lower=True)
async def commands(ans: Message):
    await addtobd(ans.peer_id)
    await ans('здарова я крутой\n⚙Доступные команды:\n/gen, /ген, /г, /g - генерация текста\n/clear - очистка базы текста для данной беседы\n/info - сколько я сгенерировал слов\n\n✉F.A.Q - https://vk.com/@vitalik1338-faq')

@bot.on.chat_message(text=['/info', 'info', '/инфо', 'инфо'], lower=True)
async def info(ans: Message):
    await addtobd(ans.peer_id)
    with open(dir_to_txt + str(ans.peer_id) + '.txt', encoding="utf8") as file:
        txt = file.read().split(",")
    await ans(f'сохранил слов: {len(txt)}')

@bot.on.chat_message(text=['/clear', '/wipe', 'wipe', 'clear'], lower=True)
async def wipe(ans: Message):
    await addtobd(ans.peer_id)
    if not await check(ans, id=ans.from_id):
        await ans('Вы не администратор беседы')
    else:
        f = open(dir_to_txt + str(ans.peer_id) + '.txt', 'w', encoding='utf8')
        f.write('')
        f.close()
        await ans('База была успешно очищена.')

@bot.on.chat_message(text=['gen', 'g', 'г', 'ген', '/gen', '/g', '/г', '/ген'])
async def chat_generate(ans: Message):
    await addtobd(ans.peer_id)
    if len(ans.text) <= 60 and ans.text != '' and ans.from_id > 0 and ans.text[:3] != '[id' and ans.text[:1] != '/': # Проверяем на допустимое сообщение
        with open(dir_to_txt + str(ans.peer_id) + '.txt', encoding="utf8") as file:
            txt = file.read().split(",")
        if len(txt) >= 4:
            generator = mc.StringGenerator(samples=txt)
            message = generator.generate_string()
            if message == '':
                return "че"
            await ans(message.lower())
        else:
            await ans('Недостаточно слов для генерации (минимум 4)')

@bot.on.chat_message()
async def chat_message(ans: Message):
    await addtobd(ans.peer_id)
    if len(ans.text) <= 60 and ans.text != '' and ans.from_id > 0 and ans.text[:3] != '[id' and ans.text[:1] != '/': # Проверяем на допустимое сообщение
        with open(dir_to_txt + str(ans.peer_id) + '.txt', "a", encoding="utf8") as f:
            f.write(ans.text + ",")
        with open(dir_to_txt + str(ans.peer_id) + '.txt', encoding="utf8") as file:
            txt = file.read().split(",")
        if len(txt) >= 4 and random.randint(0, 2) == 0:
            generator = mc.StringGenerator(samples=txt)
            message = generator.generate_string()
            if message == '':
                return "че"
            await ans(message.lower())    

@bot.on.message()
async def ls_message(ans: Message):
    await addtobd(ans.peer_id)
    if ans.text != '' and ans.from_id > 0: # Проверяем на допустимое сообщение
        with open(dir_to_txt + str(ans.peer_id) + '.txt', "a", encoding="utf8") as f:
            f.write(ans.text + ",")
        with open(dir_to_txt + str(ans.peer_id) + '.txt', encoding="utf8") as file:
            txt = file.read().split(",")
        if len(txt) >= 4 and random.randint(0, 2) == 0:
            generator = mc.StringGenerator(samples=txt)
            message = generator.generate_string()
            if message == '':
                return "че"
            await ans(message.lower())
    
bot.run_polling()
