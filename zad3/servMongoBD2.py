from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from vkbottle.bot import Bot, Message, rules
import random
from datetime import datetime, timedelta
import time

bot = Bot(token="81bea9a533ee468fd9ec03365deaf39c53370802d7fc4cac960d8f75bef4fbc5dbdc65d82a0b49daed084")

db_client = MongoClient("mongodb+srv://Oshava:9JLPx0KWRIb0dFdR@oshava.clqqsh4.mongodb.net/?retryWrites=true&w=majority")

current_db = db_client["ServoSkullBot"]

collection = current_db["users_vk_v2"]

cruiser = current_db["cruiser"]

weapon_db = {"Lasgun": {"Strength": 100, "Price": 30}}

weapon_cs = {"Bayonet_knife": {"Strength": 200, "Price": 30}}

current_planet = {
    1: {"name": "Мир Улей", "description": "Небольшой бонус в виде увеличенного опыта"},
    2: {"name": "Дикий Мир", "description": "Небольшой бонус в виде увеличенной силы"},
    3: {"name": "Мир Кузня", "description": "В разработке"},
    4: {"name": "Агромир", "description": "В разработке"}
}

roles_imperium_ig = {
    "Призывник": {"Strength": 100, "Price": 50, "limit": 0},
    "Рядовой": {"Strength": 50, "Price": 100, "limit": 0},
    "Младший капрал": {"Strength": 20, "Price": 200, "limit": 0},
    "Капрал": {"Strength": 30, "Price": 300, "limit": 0},
    "Сержант": {"Strength": 40, "Price": 400, "limit": 2},
    "Старший сержант": {"Strength": 80, "Price": 800}, "limit": 2,
    "Лейтенант": {"Strength": 150, "Price": 1500, "limit": 3},
    "Капитан": {"Strength": 170, "Price": 1700, "limit": 3},
    "Майор": {"Strength": 200, "Price": 2000, "limit": 4},
    "Подполковник": {"Strength": 220, "Price": 2200, "limit": 4},
    "Полковник": {"Strength": 300, "Price": 3000, "limit": 4},
    "Генерал майор": {"Strength": 350, "Price": 3500, "limit": 5},
    "Генерал лейтенант": {"Strength": 400, "Price": 4000, "limit": 5},
    "Генерал": {"Strength": 450, "Price": 4500, "limit": 10},
    "Лорд генерал": {"Strength": 500, "Price": 5000, "limit": 10},
    "Лорд маршал": {"Strength": 600, "Price": 6000, "limit": 10},
    "Лорд генерал милитант": {"Strength": 800, "Price": 8000, "limit": 10},
    "Лорд Командор Милитант Имперской Гвардии": {"Strength": 1000, "Price": 10000, "limit": 30}}

roles_imperium_sm = {
    "Кандидат": {"Strength": 5, "Price": 50, "limit": 0},
    "Неофит": {"Strength": 5, "Price": 50, "limit": 0},
    "Скаут": {"Strength": 5, "Price": 500, "limit": 2},
    "Опустошитель": {"Strength": 300, "Price": 1000, "limit": 3},
    "Штурмовик": {"Strength": 600, "Price": 1000, "limit": 3},
    "Тактикал": {"Strength": 900, "Price": 3000, "limit": 3},
    "Сержант": {"Strength": 900, "Price": 5000, "limit": 5},
    "Лейтенант": {"Strength": 900, "Price": 10000, "limit": 10},
    "Капитан": {"Strength": 900, "Price": 15000, "limit": 20},
    "Магистр": {"Strength": 900, "Price": 20000, "limit": 30}}

arena_roles = {
    1: {"name": "Новичок", "Strength": 7},
    2: {"name": "Начинающий", "Strength": 10},
    3: {"name": "Неизвестный", "Strength": 14},
    4: {"name": "Узнаваемый", "Strength": 17},
    5: {"name": "Известный", "Strength": 21},
    6: {"name": "Знаменитый", "Strength": 25},
    7: {"name": "Выдающийся", "Strength": 30},
    8: {"name": "Прославленный", "Strength": 35},
    9: {"name": "Ветеран", "Strength": 40},
    10: {"name": "Чемпион", "Strength": 50}}

enemy_list = {1: {"Name": "planet1", "Strength": 500},
              2: {"Name": "planet2", "Strength": 1000},
              3: {"Name": "planet3", "Strength": 2000},
              4: {"Name": "planet4", "Strength": 4000},
              5: {"Name": "planet5", "Strength": 5000},
              6: {"Name": "planet6", "Strength": 6000},
              7: {"Name": "planet7", "Strength": 7000}}


def next_rank(key, dict: dict) -> str:
    a = 1
    for i in range(len(dict)):
        dict_to_list = list(dict.keys())
        b = dict_to_list[i]
        a = a + 1
        if b == key:
            return dict_to_list[i + 1]


def reg(id, nick):
    try:
        collection.insert_one(
            {"_id": id,
             "Nickname": nick,
             "Essence": "Soul",
             "Experience": 0,
             "Strength": 2,
             "Rating": 0,
             "Planet": "Unknown",
             "Structure": "Unknown",
             "Dates": {'Date_of_Birth': {"time": datetime.utcnow(), "name": "Дата рождения"}},
             "Weapon": {"weapon_cs": None, "weapon_db": None},
             "Equipment": {"Protection": None}})
        return f"[id{id}|{nick}], спасибо за регистрацию и добро пожаловать в бета версию бота✔\n Для того чтобы узнать функции бота введите команду: Как играть."
    except DuplicateKeyError:
        return f"[id{id}|{nick}], Вы уже зарегистрированы❌"


def status(id: int):
    user_in_mongo = collection.find_one({"_id": id})
    return (f"✔Nickname = [id{id}|{user_in_mongo['Nickname']}]\n "
            f"⚔Classis = {user_in_mongo['Essence']}\n "
            f"🛡Structure = {user_in_mongo['Structure']}\n "
            f"🪐Planet = {user_in_mongo['Planet']}\n "
            f"💪Strength = {user_in_mongo['Strength']}\n "
            f"🛠Experience = {user_in_mongo['Experience']}\n"
            f"⭐Rating = {user_in_mongo['Rating']}\n")


def convert_to_preferred_format(sec):
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S", ty_res)
    return res


@bot.on.chat_message(text=["reg", "Reg"])
async def reg_handler(message: Message):
    user_name = await bot.api.users.get(message.from_id)
    await message.answer(message=f"{reg(message.from_id, user_name[0].first_name)}")


@bot.on.chat_message(text=["Планеты", "планеты"])
async def planet_handler(message: Message):
    count = 1
    current_variant = ""
    for i in range(len(current_planet)):
        current_variant = current_variant + f"\n{count}) {current_planet[count]['name']} - {current_planet[count]['description']}"
        count = count + 1
    await message.answer(message="🌍Доступные планеты на данный момент:" + current_variant)


@bot.on.chat_message(text=["Статус", "статус"])
async def status_handler(message: Message):
    try:
        await message.answer(status(message.from_id))
    except:
        await message.answer(f"Зарегистрируйтесь командой reg❌")


@bot.on.chat_message(text=[("Статус <msg>"), ("статус <msg>")])
async def status_handler(message: Message, msg):
    if "[id" in msg:
        id = int(msg.split("|")[0].replace("[id", ""))
        try:
            await message.answer(status(id))
        except:
            await message.answer(f"Пользователь не зарегистрирован")
    else:
        await message.answer("Неизвестный пользователь")


@bot.on.chat_message(text=["Кулдаун", "кулдаун"])
async def planet_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})["Dates"]
    for i in range(len(user_in_mongo)):
        name_dates = list(user_in_mongo)[i]
        a = (datetime.utcnow()-user_in_mongo[name_dates]['time']).total_seconds()
        await message.answer(f"{user_in_mongo[name_dates]['name']} - прошло {convert_to_preferred_format((datetime.utcnow()-user_in_mongo[name_dates]['time']).total_seconds())}")


@bot.on.chat_message(text=["Планеты", "планеты"])
async def planet_handler(message: Message):
    count = 1
    current_variant = ""
    for i in range(len(current_planet)):
        current_variant = current_variant + f"\n{count}) {current_planet[count]['name']} - {current_planet[count]['description']}"
        count = count + 1
    await message.answer(message="Доступные планеты на данный момент:" + current_variant)


@bot.on.chat_message(text=(["Рождение <msg>", "рождение <msg>"]))
async def born_handler(message: Message, msg):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    planet = int(msg)
    if planet in current_planet:
        if user_in_mongo["Planet"] == "Unknown":
            if random.choices([1, 0], weights=[60, 40], k=1)[0] == 1:
                if planet == 1:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Essence': "Citizen",
                                                    "Structure": "Имперский мир",
                                                    "Planet": current_planet[planet]['name'],
                                                    "Dates.Date_citizen_work.time": datetime.utcnow() - timedelta(
                                                        minutes=5),
                                                    "Dates.Date_citizen_work.name": "Работа",
                                                    "Dates.Date_fight.time": datetime.utcnow() - timedelta(
                                                        minutes=10),
                                                    "Dates.Date_fight.name": "Спуститься"},
                                           '$inc': {'Experience': 20}
                                           })
                    await message.answer(message=f"✔[id{message.from_id}|{user_in_mongo['Nickname']}],"
                                                 f"твой путь начинается с того, что ты родился в жилом уровне Мира-Улья."
                                                 f"Великие ульи не похожи на прочие миры Империума, "
                                                 f"а ты – на жителей  тех миров. Ты  с детства познаешь, что такое тяжелая работа в фабриках империума,"
                                                 f" производя аммуницию и выполняя норму.",
                                         attachment=random.choice(
                                             ["photo-212919678_457239027", "photo-212919678_457239026"]))
                elif planet == 2:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Essence': "Savage",
                                                    "Structure": "Имперский мир",
                                                    "Planet": current_planet[planet]['name'],
                                                    "Dates.Date_citizen_work.time": datetime.utcnow() - timedelta(
                                                        minutes=5),
                                                    "Dates.Date_citizen_work.name": "Охота",
                                                    "Dates.Date_fight.time": datetime.utcnow() - timedelta(
                                                        minutes=10),
                                                    "Dates.Date_fight.name": "Арена"},
                                           '$inc': {'Strength': 2}
                                           })
                    await message.answer(message=f"✔[id{message.from_id}|{user_in_mongo['Nickname']}], большая часть твоей жизни прошла среди твоего племени на жестоком диком мире, "
                                                 f"где сила, отвага и боевое искусство ценится превыше всего. "
                                                 f"Ты большой, сильный и храбрый,  но  при  этом  еще  и  суеверный.  "
                                                 f"Ты  почти  наверняка принадлежишь  к  воинственному  клану,  и  ценят  тебя  за твои боевые умения",
                                         attachment=random.choice(
                                             ["photo-212919678_457239033", "photo-212919678_457239032"]))
                else:
                    await message.answer(message="Данной планеты не существует либо еще не разработана")
            else:
                await message.answer(
                    message="К сожалению вы погибли при рождении❌. Попробуйте написать команду снова",
                    attachment="photo-212919678_457239022")
        else:
            await message.answer(message="Вы уже рождены")
    else:
        await message.answer(message="Данной планеты либо не существует, либо еще не добавлена")


@bot.on.chat_message(text=["Работать", "работать"])
async def work_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Planet"] == "Мир Улей":
        a = user_in_mongo['Dates']['Date_citizen_work']["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() > 300:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы отправились на работу выполнять свои обязанности")
            if random.choices(["win", "defeat"], weights=[70, 30], k=1)[0] == "win":
                collection.update_one({'_id': message.from_id},
                                      {'$set': {'Dates.Date_citizen_work.time': datetime.utcnow()},
                                       '$inc': {'Experience': 10, "Strength": 2}})
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], сегодня на работе не произошло ничего необычного.\n"
                            "Опыт повышен на 10 пунктов, сила на 2")
            else:
                aboba = random.choices([1, 2, 3])
                if aboba == 1:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Dates.Date_citizen_work.time': datetime.utcnow()},
                                           '$inc': {'Experience': 5, "Strength": 1}})
                    await message.answer(
                        message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], из-за поломки вы не успели выполнить норму. Опыт повышен на 5, а сила на 1")
                elif aboba == 2:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Dates.Date_citizen_work.time': datetime.utcnow()}})
                    await message.answer(
                        message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], во время работы на вас напали бандиты. Вы успели сбежать")
                elif aboba == 3:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Dates.Date_citizen_work.time': datetime.utcnow()},
                                           '$inc': {'Experience': 20, "Strength": 4}})
                    await message.answer(
                        message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы перевыполнили норму, ваш опыт повышен на 20, сила на 4")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], отдохните. Кд работы 5 минут")


@bot.on.chat_message(text=["Спуститься", "спуститься"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Мир Улей":
        await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], выберите куда спуститься и напишите: \nСпуститься название_места (Пример Спуститься Древние фабрики)\n1)Древние фабрики\n2)Подулье\n3)Дно улья")


@bot.on.chat_message(text=["Спуститься <msg>", "спуститься <msg>"])
async def work_handler(message: Message, msg):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Planet"] == "Мир Улей":
        a = user_in_mongo['Dates']['Date_fight']["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() > 600:
            if msg == "Древние фабрики":
                enemy_strength = random.uniform(1, 6)
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы спустились в Древние фабрики")
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вам на пути попалась редкая тварь с силой: {enemy_strength}")
                aboba = random.choices(["win_self", "win_opp"],
                                       weights=[user_in_mongo["Strength"], enemy_strength], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (
                                user_in_mongo["Strength"] + enemy_strength))) + 2
                    collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_fight.time": datetime.utcnow()}, "$inc": {"Strength": rating_current}})
                    await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы победили! Опыт повышен на {rating_current}")
                else:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Dates.Date_fight.time': datetime.utcnow()}})
                    await message.answer(
                        message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы проиграли и отступаете")
            elif msg == "Подулье":
                enemy_strength = random.uniform(20, 40)
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы спустились в Подулье")
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вам на пути попалась редкая тварь с силой: {enemy_strength}")
                aboba = random.choices(["win_self", "win_opp"],
                                       weights=[user_in_mongo["Strength"], enemy_strength], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (
                                user_in_mongo["Strength"] + enemy_strength))) + 2
                    collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_fight.time": datetime.utcnow()}, "$inc": {"Strength": rating_current}})
                    await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы победили! Опыт повышен на {rating_current}")
                else:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Dates.Date_fight.time': datetime.utcnow()}})
                    await message.answer(
                        message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы проиграли и отступаете")
            elif msg == "Дно улья":
                enemy_strength = random.uniform(40, 100)
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы спустились в Дно улья")
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вам на пути попалась редкая тварь с силой: {enemy_strength}")
                aboba = random.choices(["win_self", "win_opp"],
                                       weights=[user_in_mongo["Strength"], enemy_strength], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (
                                user_in_mongo["Strength"] + enemy_strength))) + 2
                    collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_fight.time": datetime.utcnow()}, "$inc": {"Strength": rating_current}})
                    await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы победили! Опыт повышен на {rating_current}")
                else:
                    collection.update_one({'_id': message.from_id},
                                          {'$set': {'Dates.Date_fight.time': datetime.utcnow()}})
                    await message.answer(
                        message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы проиграли и отступаете")
            else:
                await message.answer(message="Неизвестная локация")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], отдохните. Кд 10 минут")


@bot.on.chat_message(text=["Охота", "охота"])
async def work_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Planet"] == "Дикий Мир":
        a = user_in_mongo['Dates']['Date_citizen_work']["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() > 300:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы отправились на охоту")
            if random.choices(["win", "defeat"], weights=[90, 10], k=1)[0] == "win":
                collection.update_one({'_id': message.from_id},
                                      {'$set': {'Dates.Date_citizen_work.time': datetime.utcnow()},
                                       '$inc': {'Experience': 10, "Strength": 2}})
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Сегодня на охоте не произошло ничего необычного.\n"
                            "Опыт повышен на 10 пунктов, сила на 2")
            else:
                collection.update_one({'_id': message.from_id},
                                      {'$set': {'Dates.Date_citizen_work.time': datetime.utcnow()}})
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Охота прошла неудачно")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], отдохните. Кд охоты 5 минут")


@bot.on.chat_message(text=["Арена", "арена"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Дикий Мир":
        current_message = f"[id{message.from_id}|{user_in_mongo['Nickname']}], выберите противника и напишите: \nАрена номер (Пример Арена 2)"
        count = 0
        for i in range(len(arena_roles)):
            count = count + 1
            name_dates = arena_roles[count]
            current_message = current_message + f"\n{count}) {name_dates['name']} - {name_dates['Strength']}"
        await message.answer(current_message)


@bot.on.chat_message(text=["Арена <msg>", "арена <msg>"])
async def info_handler(message: Message, msg):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    number_opp = int(msg)
    if user_in_mongo["Planet"] == "Дикий Мир":
        a = user_in_mongo['Dates']['Date_fight']["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() > 600:
            if number_opp == 10:
                aboba = random.choices(["win_self", "win_opp"], weights=[user_in_mongo["Strength"], arena_roles[number_opp]["Strength"]], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (user_in_mongo["Strength"] + arena_roles[number_opp]["Strength"]))) + 2
                    collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_fight.time": datetime.utcnow()},
                                                                     "$inc": {"Strength": rating_current}})
                    await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы победили ваша сила увеличина на {rating_current}")
                else:
                    collection.update_one({"_id": message.from_id}, {"$set" : {"Dates.Date_fight.time": datetime.utcnow()}})
                    await message.answer("Defeat")
            elif arena_roles[number_opp]["Strength"] < user_in_mongo["Strength"]:
                await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], выберите противника посильнее")
            else:
                aboba = random.choices(["win_self", "win_opp"], weights=[user_in_mongo["Strength"], arena_roles[number_opp]["Strength"]], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (user_in_mongo["Strength"] + arena_roles[number_opp]["Strength"]))) + 2
                    collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_fight.time": datetime.utcnow()},
                                                                     "$inc": {"Strength": rating_current}})
                    await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы победили ваша сила увеличина на {rating_current}")
                else:
                    collection.update_one({"_id": message.from_id}, {"$set" : {"Dates.Date_fight.time": datetime.utcnow()}})
                    await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы проиграли, восстановите силы и попытайте удачу снова")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Отдохните. Кд арены 10 минут")


@bot.on.chat_message(text=["Вступить ИГ", "Вступление Имперская Гвардия", "Вступление ИГ", "вступление ИГ",
                           "вступление ммперская гвардия", "вступить ммперская гвардия"])
async def roles_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже состоите имперской гвардии")
    elif user_in_mongo["Essence"] in roles_imperium_sm:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже состоите в структуре Космодесанта")
    elif user_in_mongo["Planet"] in str(current_planet):
        if user_in_mongo["Experience"] >= 50:
            collection.update_one({'_id': message.from_id},
                                  {'$set': {'Essence': "Призывник",
                                            'Structure': "Астра Милитарум",
                                            "Dates.Date_ig_Shooting.time": datetime.utcnow() - timedelta(
                                                minutes=1440), "Dates.Date_ig_Shooting.name": "Стрельбище",
                                            "Dates.Date_ig_Workout.time": datetime.utcnow() - timedelta(
                                                minutes=1440), "Dates.Date_ig_Workout.name": "Тренировка",
                                            "Dates.Date_ig_vaxta.time": datetime.utcnow() - timedelta(
                                                minutes=1440), "Dates.Date_ig_vaxta.name": "Вахта",
                                            "Dates.Date_ig_crusade.time": datetime.utcnow() - timedelta(
                                                minutes=1440), "Dates.Date_ig_crusade.name": "Поход",
                                            "Weapon.weapon_db": weapon_db["Lasgun"],
                                            "Weapon.weapon_cs": weapon_cs["Bayonet_knife"]},
                                   '$inc': {"Strength": 100,
                                            'Experience': -50},
                                   '$unset': {"Dates.Date_citizen_work": 1,
                                              "Dates.Date_fight": 1}})
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы вступили в имперскую гвардию Ваше звание: Призывник.")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Недостаточно опыта")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы не зарегистрированы. Зарегистрируйтесь в реестр бойцов reg")


@bot.on.chat_message(text=["Получить повышение", "Повышение", "повышение", "получить повышение"])
async def roles_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] == "Кандидат":
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Пройдите Имплантацию")
    elif user_in_mongo["Essence"] == "Неофит":
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Используйте команду Стать Скаутом")
    elif user_in_mongo["Essence"] == "Скаут":
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], Используйте команду Последняя Имплантация")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        role = next_rank(user_in_mongo["Essence"], roles_imperium_ig)
        price = roles_imperium_ig[role]["Price"]
        if user_in_mongo["Experience"] >= price:
            strength = roles_imperium_ig[role]['Strength']
            collection.update_one({'_id': message.from_id},
                                  {'$set': {'Essence': role}, '$inc': {'Experience': -price, 'Strength': strength}})
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы были повышены до {role}, ваш опыт был уменьшен на {price} и повышены статы")
        else:
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Недосточно опыта, необходимо {price}")
    elif user_in_mongo["Essence"] in roles_imperium_sm:
            role = next_rank(user_in_mongo["Essence"], roles_imperium_sm)
            price = roles_imperium_sm[role]["Price"]
            if user_in_mongo["Experience"] >= price:
                strength = roles_imperium_sm[role]['Strength']
                collection.update_one({'_id': message.from_id},
                                      {'$set': {'Essence': role}, '$inc': {'Experience': -price, 'Strength': strength}})
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы были повышены до {role}, ваш опыт был уменьшен на {price} и повышены статы")
            else:
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Недосточно опыта, необходимо {price}")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы не зарегистрированы. Зарегистрируйтесь в реестр бойцов reg")


@bot.on.chat_message(text=["Тренировка", "тренировка"])
async def charge_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        a = user_in_mongo["Dates"]["Date_ig_Workout"]["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() >= 1800:
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], успешно провел тренировку. Опыт повышен на 20, сила на 1. Следующая тренировка через пол часа")
            collection.update_one({'_id': message.from_id},
                                  {'$set': {"Dates.Date_ig_Workout.time": datetime.utcnow()},
                                   '$inc': {'Experience': 20, 'Strength': 1}})
        else:
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были на тренировке! Кд пол часа")
    elif user_in_mongo["Essence"] in roles_imperium_sm:
        if user_in_mongo["Essence"] == "Кандидат":
            a = user_in_mongo["Dates"]["Date_sm_Workout"]["time"]
            b = datetime.utcnow()
            c = b - a
            if c.total_seconds() >= 300:
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], успешно провел тренировку. Опыт повышен на 20, сила на 3. Следующая тренировка через 5 минут")
                collection.update_one({'_id': message.from_id},
                                      {'$set': {"Dates.Date_sm_Workout.time": datetime.utcnow()},
                                       '$inc': {'Experience': 20, 'Strength': 3}})
            else:
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были на тренировке! Кд 5 минут")
        else:
            a = user_in_mongo["Dates"]["Date_sm_Workout"]["time"]
            b = datetime.utcnow()
            c = b - a
            if c.total_seconds() >= 1800:
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], успешно провел тренировку. Опыт повышен на 10, сила на 0.5. Следующая тренировка через пол часа")
                collection.update_one({'_id': message.from_id},
                                      {'$set': {"Dates.Date_sm_Workout.time": datetime.utcnow()},
                                       '$inc': {'Experience': 10, 'Strength': 0.5}})
            else:
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были на тренировке! Кд пол часа")


@bot.on.chat_message(text=["Стрельбище", "стрельбище"])
async def charge_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in str(roles_imperium_ig):
        a = user_in_mongo["Dates"]["Date_ig_Shooting"]["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() >= 3600:
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], успешно провел тренировку на стрельбище. Опыт повышен на 10, сила на 1")
            collection.update_one({'_id': message.from_id},
                                  {'$set': {"Dates.Date_ig_Shooting.time": datetime.utcnow()},
                                   '$inc': {'Experience': 10, 'Strength': 1}})
        else:
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были на стрельбище! КД час")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вступите в Имперскую Гвардию!")


@bot.on.chat_message(text=["Вахта", "вахта"])
async def charge_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in str(roles_imperium_ig):
        a = user_in_mongo["Dates"]["Date_ig_vaxta"]["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() >= 3600:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы отправились на вахту. Опыт повышен на 10, сила на 1")
            collection.update_one({'_id': message.from_id},
                                  {'$set': {"Dates.Date_ig_vaxta.time": datetime.utcnow()},
                                   '$inc': {'Experience': 10, 'Strength': 1}})
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были на вахте! Кд час")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вступите в Имперскую Гвардию!")


@bot.on.chat_message(text=["Стать Кандидатом", "стать кандидатом", "Стать кандидатом"])
async def roles_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже состоите имперской гвардии")
    elif user_in_mongo["Essence"] in roles_imperium_sm:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже состоите в структуре Космодесанта")
    elif user_in_mongo["Planet"] in str(current_planet):
        if user_in_mongo["Strength"] >= 50:
            if user_in_mongo["Experience"] >= 50:
                collection.update_one({'_id': message.from_id},
                                      {'$set': {'Essence': "Кандидат",
                                                'Structure': "Космодесант",
                                                "Dates.Date_sm_implants.time": datetime.utcnow() - timedelta(
                                                    minutes=40), "Dates.Date_sm_implants.name": "Имплантация",
                                                "Dates.Date_sm_Workout.time": datetime.utcnow() - timedelta(
                                                    minutes=30), "Dates.Date_sm_Workout.name": "Тренировка",
                                                "implants": "0/19",
                                                "Chemical_processing": False},
                                       '$inc': {"Strength": 5,
                                                'Experience': -50},
                                       '$unset': {"Dates.Date_citizen_work": 1,
                                                  "Dates.Date_fight": 1}})
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вас приняли как Кандидата в космодесант.")
            else:
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Недостаточно опыта")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы слишком слабы")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы не зарегистрированы. Зарегистрируйтесь в реестр бойцов reg")


@bot.on.chat_message(text=["Химическая обработка", "хим обработка"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] == "Кандидат":
        if user_in_mongo["Chemical_processing"] == False:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}],Вы проходите химическую обработку")
            collection.update_one({"_id": message.from_id}, {"$set": {"Chemical_processing": True}})
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вам не требуется химическая обработка")


@bot.on.chat_message(text=["Гипнотерапия", "гипнотерапия"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] == "Кандидат":
        if user_in_mongo["Hypnotherapy"] == False:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}],Вы проходите Гипнотерапию")
            collection.update_one({"_id": message.from_id}, {"$set": {"Hypnotherapy": True}})
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вам не требуется Гипнотерапия")

implants_0_5 = ["0/19", "3/19", "5/19"]
implants_6_13 = ["6/19", "9/19", "13/19", "15/19"]

@bot.on.chat_message(text=["Имплантация", "имплантация"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] == "Кандидат":
        a = user_in_mongo['Dates']['Date_sm_implants']["time"]
        b = datetime.utcnow()
        c = b - a
        if user_in_mongo["Chemical_processing"] == False:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], перед имплантацией Вам требуется пройти химическую обработку")
        elif user_in_mongo["Experience"] < 50:
            await message.answer(message="Недостаточно опыта")
        elif c.total_seconds() >= 1200:
            if user_in_mongo["implants"] == "0/19":
                collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                Heart = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 60-user_in_mongo["Strength"]], k=1)[0]
                Ossmodula = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 60-user_in_mongo["Strength"]], k=1)[0]
                Biscopia = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 60-user_in_mongo["Strength"]], k=1)[0]
                await message.answer(message="⚙Вживление импланта: Второе сердце")
                if Heart == "Success":
                    await message.answer(message="Успех!")
                    await message.answer(message="⚙Вживление импланта: Оссмодула")
                    if Ossmodula == "Success":
                        await message.answer(message="Успех!")
                        await message.answer(message="⚙Вживление импланта: Бископия")
                        if Biscopia == "Success":
                            await message.answer(message="Успех!")
                            collection.update_one({"_id": message.from_id},
                                                  {"$set": {"implants": "3/19", "Chemical_processing": False},
                                                   "$inc": {"Experience": -50, "Strength": 2}})
                        else:
                            await message.answer(message="Операция прошла неудачно...")
                            collection.update_one({"_id": message.from_id},
                                                  {"$set": {"Chemical_processing": False},
                                                   "$inc": {"Experience": -(user_in_mongo["Experience"]/2),
                                                            "Strength": -(user_in_mongo["Strength"]/2)}})
                    else:
                        await message.answer(message="Операция прошла неудачно...")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"Chemical_processing": False},
                                               "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                        "Strength": -(user_in_mongo["Strength"] / 2)}})
                else:
                    await message.answer(message="Операция прошла неудачно...")
                    collection.update_one({"_id": message.from_id},
                                          {"$set": {"Chemical_processing": False},
                                           "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                    "Strength": -(user_in_mongo["Strength"] / 2)}})
            elif user_in_mongo["implants"] == "3/19":
                collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                Gemastamen = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 70-user_in_mongo["Strength"]], k=1)[0]
                Larraman = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 70-user_in_mongo["Strength"]], k=1)[0]
                await message.answer(message="⚙Вживление импланта: Гемастамен")
                if Gemastamen == "Success":
                    await message.answer(message="Успех!")
                    await message.answer(message="⚙Вживление импланта: Орган Ларрамана")
                    if Larraman == "Success":
                        await message.answer(message="Успех!")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"implants": "5/19", "Chemical_processing": False},
                                               "$inc": {"Experience": -50, "Strength": 2}})
                    else:
                        await message.answer(message="Операция прошла неудачно...")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"Chemical_processing": False},
                                               "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                        "Strength": -(user_in_mongo["Strength"] / 2)}})
                else:
                    await message.answer(message="Операция прошла неудачно...")
                    collection.update_one({"_id": message.from_id},
                                          {"$set": {"Chemical_processing": False},
                                           "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                    "Strength": -(user_in_mongo["Strength"] / 2)}})
            elif user_in_mongo["implants"] == "5/19":
                collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                Cataleptic_Knot = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 80-user_in_mongo["Strength"]], k=1)[0]
                await message.answer(message="⚙Вживление импланта: Каталептический Узел")
                if Cataleptic_Knot == "Success":
                    await message.answer(message="Успех! С этого этапа вы должны будете проходить Гипнотерапию, "
                                                 "чтобы органы лучше контролировать свои органы")
                    collection.update_one({"_id": message.from_id},
                                          {"$set": {"implants": "6/19", "Chemical_processing": False, "Hypnotherapy": False},
                                           "$inc": {"Experience": -50, "Strength": 3}})
                else:
                    await message.answer(message="Операция прошла неудачно...")
                    collection.update_one({"_id": message.from_id},
                                          {"$set": {"Chemical_processing": False},
                                           "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                    "Strength": -(user_in_mongo["Strength"] / 2)}})
            elif user_in_mongo["implants"] == "6/19":
                if user_in_mongo["Hypnotherapy"] == True:
                    collection.update_one({"_id": message.from_id},
                                          {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                    Preomnor = random.choices(["Success", "Fail"],
                                              weights=[user_in_mongo["Strength"], 90 - user_in_mongo["Strength"]], k=1)[0]
                    Omophagy = random.choices(["Success", "Fail"],
                                              weights=[user_in_mongo["Strength"], 90 - user_in_mongo["Strength"]], k=1)[0]
                    Multilung = random.choices(["Success", "Fail"],
                                               weights=[user_in_mongo["Strength"], 90 - user_in_mongo["Strength"]], k=1)[0]
                    await message.answer(message="⚙Вживление импланта: Преомнор")
                    if Preomnor == "Success":
                        await message.answer(message="Успех!")
                        await message.answer(message="⚙Вживление импланта: Омофагия")
                        if Omophagy == "Success":
                            await message.answer(message="Успех!")
                            await message.answer(message="⚙Вживление импланта: Мультилегкое")
                            if Multilung == "Success":
                                await message.answer(message="Успех!")
                                collection.update_one({"_id": message.from_id},
                                                      {"$set": {"implants": "9/19", "Chemical_processing": False,
                                                                "Hypnotherapy": False},
                                                       "$inc": {"Experience": -50, "Strength": 2}})
                            else:
                                await message.answer(message="Операция прошла неудачно...")
                                collection.update_one({"_id": message.from_id},
                                                      {"$set": {"Chemical_processing": False,
                                                                "Hypnotherapy": False},
                                                       "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                                "Strength": -(user_in_mongo["Strength"] / 2)}})
                        else:
                            await message.answer(message="Операция прошла неудачно...")
                            collection.update_one({"_id": message.from_id},
                                                  {"$set": {"Chemical_processing": False,
                                                            "Hypnotherapy": False},
                                                   "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                            "Strength": -(user_in_mongo["Strength"] / 2)}})
                    else:
                        await message.answer(message="Операция прошла неудачно...")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"Chemical_processing": False,
                                                        "Hypnotherapy": False},
                                               "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                        "Strength": -(user_in_mongo["Strength"] / 2)}})
                else:
                    await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], пройдите Гипнотерапию!")
            elif user_in_mongo["implants"] == "9/19":
                if user_in_mongo["Hypnotherapy"] == True:
                    collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                    Occuloba = random.choices(["Success", "Fail"],
                                              weights=[user_in_mongo["Strength"], 100 - user_in_mongo["Strength"]], k=1)[0]
                    Limans_ear = random.choices(["Success", "Fail"],
                                                weights=[user_in_mongo["Strength"], 100 - user_in_mongo["Strength"]], k=1)[0]
                    Anabiotic_Membrane = random.choices(["Success", "Fail"],
                                                        weights=[user_in_mongo["Strength"], 100 - user_in_mongo["Strength"]], k=1)[0]
                    Melanochromic_Organ = random.choices(["Success", "Fail"],
                                                         weights=[user_in_mongo["Strength"], 100 - user_in_mongo["Strength"]], k=1)[0]
                    await message.answer(message="⚙Вживление импланта: Оккулоба")
                    if Occuloba == "Success":
                        await message.answer(message="Успех!")
                        await message.answer(message="⚙Вживление импланта: Ухо Лимана")
                        if Limans_ear == "Success":
                            await message.answer(message="Успех!")
                            await message.answer(message="⚙Вживление импланта: Анабиозная Мембрана")
                            if Anabiotic_Membrane == "Success":
                                await message.answer(message="Успех!")
                                await message.answer(message="⚙Вживление импланта: Меланохромический Орган")
                                if Melanochromic_Organ == "Success":
                                    await message.answer(message="Успех!")
                                    collection.update_one({"_id": message.from_id},
                                                          {"$set": {"implants": "13/19", "Chemical_processing": False,
                                                                    "Hypnotherapy": False},
                                                           "$inc": {"Experience": -50, "Strength": 3}})
                                else:
                                    await message.answer(message="Операция прошла неудачно...")
                                    collection.update_one({"_id": message.from_id},
                                                          {"$set": {"Chemical_processing": False,
                                                                    "Hypnotherapy": False},
                                                           "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                                    "Strength": -(user_in_mongo["Strength"] / 2)}})
                            else:
                                await message.answer(message="Операция прошла неудачно...")
                                collection.update_one({"_id": message.from_id},
                                                      {"$set": {"Chemical_processing": False,
                                                                "Hypnotherapy": False},
                                                       "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                                "Strength": -(user_in_mongo["Strength"] / 2)}})
                        else:
                            await message.answer(message="Операция прошла неудачно...")
                            collection.update_one({"_id": message.from_id},
                                                  {"$set": {"Chemical_processing": False,
                                                            "Hypnotherapy": False},
                                                   "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                            "Strength": -(user_in_mongo["Strength"] / 2)}})
                    else:
                        await message.answer(message="Операция прошла неудачно...")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"Chemical_processing": False,
                                                        "Hypnotherapy": False},
                                               "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                        "Strength": -(user_in_mongo["Strength"] / 2)}})
                else:
                    await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], пройдите Гипнотерапию!")
            elif user_in_mongo["implants"] == "13/19":
                collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                Oolitic_Bud = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 120 - user_in_mongo["Strength"]], k=1)[0]
                Neuroglottis = random.choices(["Success", "Fail"], weights=[user_in_mongo["Strength"], 120 - user_in_mongo["Strength"]], k=1)[0]
                await message.answer(message="⚙Вживление импланта: Оолитовая Почка")
                if Oolitic_Bud == "Success":
                    await message.answer(message="Успех!")
                    await message.answer(message="⚙Вживление импланта: Нейроглоттис")
                    if Neuroglottis == "Success":
                        await message.answer(message="Успех!")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"implants": "15/19", "Chemical_processing": False,
                                                        "Hypnotherapy": False},
                                               "$inc": {"Experience": -50, "Strength": 3}})
                    else:
                        await message.answer(message="Операция прошла неудачно...")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"Chemical_processing": False,
                                                        "Hypnotherapy": False},
                                               "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                        "Strength": -(user_in_mongo["Strength"] / 2)}})
                else:
                    await message.answer(message="Операция прошла неудачно...")
                    collection.update_one({"_id": message.from_id},
                                          {"$set": {"Chemical_processing": False,
                                                    "Hypnotherapy": False},
                                           "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                    "Strength": -(user_in_mongo["Strength"] / 2)}})
            elif user_in_mongo["implants"] == "15/19":
                collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_sm_implants.time": datetime.utcnow()}})
                if user_in_mongo["Hypnotherapy"] == True:
                    mucranoid = random.choices(["Success", "Fail"],
                                              weights=[user_in_mongo["Strength"], 150 - user_in_mongo["Strength"]], k=1)[0]
                    Betchers_iron = random.choices(["Success", "Fail"],
                                              weights=[user_in_mongo["Strength"], 150 - user_in_mongo["Strength"]], k=1)[0]
                    Progenoids = random.choices(["Success", "Fail"],
                                               weights=[user_in_mongo["Strength"], 150 - user_in_mongo["Strength"]], k=1)[0]
                    await message.answer(message="⚙Вживление импланта: Мукраноид")
                    if mucranoid == "Success":
                        await message.answer(message="Успех!")
                        await message.answer(message="⚙Вживление импланта: Железа Бетчера")
                        if Betchers_iron == "Success":
                            await message.answer(message="Успех!")
                            await message.answer(message="⚙Вживление импланта: Прогеноиды")
                            if Progenoids == "Success":
                                await message.answer(message="Успех! С этого этапа вы можете начать обучение скаутом")
                                collection.update_one({"_id": message.from_id},
                                                      {"$set": {"implants": "18/19", "Essence": "Неофит", "Chemical_processing": False},
                                                       "$inc": {"Experience": -50, "Strength": 3},
                                                       "$unset": {"Hypnotherapy": 1}})
                            else:
                                await message.answer(message="Операция прошла неудачно...")
                                collection.update_one({"_id": message.from_id},
                                                      {"$set": {"Chemical_processing": False,
                                                                "Hypnotherapy": False},
                                                       "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                                "Strength": -(user_in_mongo["Strength"] / 2)}})
                        else:
                            await message.answer(message="Операция прошла неудачно...")
                            collection.update_one({"_id": message.from_id},
                                                  {"$set": {"Chemical_processing": False,
                                                            "Hypnotherapy": False},
                                                   "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                            "Strength": -(user_in_mongo["Strength"] / 2)}})
                    else:
                        await message.answer(message="Операция прошла неудачно...")
                        collection.update_one({"_id": message.from_id},
                                              {"$set": {"Chemical_processing": False,
                                                        "Hypnotherapy": False},
                                               "$inc": {"Experience": -(user_in_mongo["Experience"] / 2),
                                                        "Strength": -(user_in_mongo["Strength"] / 2)}})
                else:
                    await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], пройдите Гипнотерапию!")
        else:
            await message.answer(message="Между имплантациями должно пройти 20 минут")


@bot.on.chat_message(text=["Стать Скаутом"])
async def roles_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже состоите имперской гвардии")
    elif user_in_mongo["Planet"] in str(current_planet):
        if user_in_mongo["Essence"] == "Неофит":
            collection.update_one({'_id': message.from_id},
                                  {'$set': {'Essence': "Скаут",
                                            "Dates.Date_sm_Workout.time": datetime.utcnow() - timedelta(
                                                minutes=30), "Dates.Date_sm_Workout.name": "Тренировка",
                                            "Dates.Date_ig_crusade.time": datetime.utcnow() - timedelta(
                                                minutes=1440), "Dates.Date_ig_crusade.name": "Поход"},
                                   '$inc': {"Strength": 5},
                                   '$unset': {"Dates.Date_sm_implants": 1,"Chemical_processing": 1,"Hypnotherapy":1}})
            await message.answer(
                message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы успешно дожили до Скаута.")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], недостаточно имплантов")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы не зарегистрированы. Зарегистрируйтесь в реестр бойцов reg")


@bot.on.chat_message(text=["Последняя имплантация"])
async def roles_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Выберете одну из планет для рождения. Для списка планет введите команду: Планеты")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже состоите имперской гвардии")
    elif user_in_mongo["Planet"] in str(current_planet):
        if user_in_mongo["Essence"] == "Скаут":
            if user_in_mongo["Experience"] >= 500:
                collection.update_one({'_id': message.from_id},
                                      {'$set': {'Essence': "Опустошитель",
                                                "Dates.Date_sm_Workout.time": datetime.utcnow() - timedelta(
                                                    minutes=30), "Dates.Date_sm_Workout.name": "Тренировка"},
                                       '$inc': {"Strength": 300,
                                                'Experience': -500},
                                       })
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], вас повысили до опустошителя")
            else:
                await message.answer(
                    message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], недосточно опыта. Нужно 500")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], недостаточно имплантов")
    else:
        await message.answer(
            message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы не зарегистрированы. Зарегистрируйтесь в реестр бойцов reg")


@bot.on.chat_message(text="Собрать поход")
async def help_handler(message: Message):
    current_message = f"[id{message.from_id}|{collection.find_one({'_id': message.from_id})['Nickname']}], Список врагов для похода\n"
    count = 1
    for i in range(len(enemy_list)):
        current_message = current_message + f"{count}) {enemy_list[count]['Name']}, мощь - {enemy_list[count]['Strength']}\n"
        count = count + 1
    await message.answer(current_message)


@bot.on.chat_message(text="Собрать поход <msg>")
async def help_handler(message: Message, msg):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] in roles_imperium_sm:
        if roles_imperium_sm[user_in_mongo["Essence"]]["limit"] >= 1:
            a = user_in_mongo['Dates']['Date_ig_crusade']["time"]
            b = datetime.utcnow()
            c = b - a
            if c.total_seconds() >= 10800:
                role = roles_imperium_sm[user_in_mongo["Essence"]]["limit"]
                mes = int(msg)
                if mes in enemy_list:
                    current = str(list(cruiser.find()))
                    if str(message.from_id) in current:
                        await message.answer(message="Вы уже на корабле")
                    else:
                        try:
                            cruiser.insert_one(
                                {'_id': message.from_id,
                                 "Nickname": user_in_mongo["Nickname"],
                                 "limit": role,
                                 "objective": mes,
                                 "Strength": user_in_mongo["Strength"],
                                 "peer_id": message.peer_id,
                                 "partners": {}}
                            )
                            await message.answer(message=f"Корабль готовится к отправлению.\n Номер: {message.from_id}")
                        except DuplicateKeyError:
                            await message.answer(message="Вы уже создали ивент")
            else:
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были в походе")
        else:
            await message.answer(message="Звание не позволяет Вам собирать походы!")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        if roles_imperium_ig[user_in_mongo["Essence"]]["limit"] >= 1:
            a = user_in_mongo['Dates']['Date_ig_crusade']["time"]
            b = datetime.utcnow()
            c = b - a
            if c.total_seconds() >= 10800:
                role = roles_imperium_ig[user_in_mongo["Essence"]]["limit"]
                mes = int(msg)
                if mes in enemy_list:
                    current = str(list(cruiser.find()))
                    if str(message.from_id) in current:
                        await message.answer(message="Вы уже на корабле")
                    else:
                        try:
                            cruiser.insert_one(
                                {'_id': message.from_id,
                                 "Nickname": user_in_mongo["Nickname"],
                                 "limit": role,
                                 "objective": mes,
                                 "Strength": user_in_mongo["Strength"],
                                 "peer_id": message.peer_id,
                                 "partners": {}}
                            )
                            await message.answer(message=f"Корабль готовится к отправлению.\n Номер: {message.from_id}")
                        except DuplicateKeyError:
                            await message.answer(message="Вы уже создали ивент")
            else:
                await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были в походе")
        else:
            await message.answer(message="Звание не позволяет Вам собирать походы!")


@bot.on.chat_message(text="Поход <msg>")
async def help_handler(message: Message, msg):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] == "Призывник":
        await message.answer(message="Вам не закончили обучение и вам еще рано отправлятся в походы")
    elif user_in_mongo["Essence"] == "Кандидат":
        await message.answer(message="Вам не закончили обучение и вам еще рано отправлятся в походы")
    else:
        a = user_in_mongo['Dates']['Date_ig_crusade']["time"]
        b = datetime.utcnow()
        c = b - a
        if c.total_seconds() >= 10800:
            current = str(list(cruiser.find()))
            if msg in current:
                cruiser_id = cruiser.find_one({"_id": int(msg)})
                if str(message.from_id) in current:
                    await message.answer(message="Вы уже в корабле")
                elif cruiser_id["limit"] == len(cruiser_id["partners"]):
                    await message.answer(message="Корабль уже заполнен")
                else:
                    int_msg = int(msg)
                    cruiser.update_one({"_id": int_msg}, {"$set": {f"partners.{message.from_id}": {"peer_id": message.peer_id}}, "$inc": {"Strength": user_in_mongo["Strength"]}})
                    await message.answer(message="Вы поступили в расположение корабля")
            else:
                await message.answer(message="Данного корабля не существует")
        else:
            await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], Вы уже были в походе")


@bot.on.chat_message(text="Поход")
async def help_handler(message: Message):
    cruiser_ha = cruiser.find()
    current_mess = "Для того чтобы отправится в поход, создайте свой корабль или зайдите в существующий командой:\nПоход Номер корабля (Пример Поход 111111)"
    count = 0
    for i in cruiser_ha:
        count = count + 1
        current_mess = current_mess + f"\n{count})Цель - {enemy_list[i['objective']]['Name']} Номер корабля - {i['_id']}, Создатель - [id{i['_id']}|{i['Nickname']}], Занято - {len(i['partners'])}/{i['limit']}, общая сила {i['Strength']}"
    await message.answer(current_mess)


@bot.on.chat_message(text="Состав корабля")
async def help_handler(message: Message):
    current_mess = "Состав похода:"
    cruiser_id = cruiser.find_one({"_id": message.from_id})
    count = 0
    for i in range(len(cruiser_id["partners"])):
        user_in_mongo = collection.find_one({"_id": int(list(cruiser_id["partners"])[i])})
        count = count + 1
        current_mess = current_mess + f"\n{count}) [id{list(cruiser_id['partners'])[i]}|{user_in_mongo['Nickname']}] - {user_in_mongo['Essence']}, сила - {user_in_mongo['Strength']}"
    await message.answer(current_mess)


@bot.on.chat_message(text="Сброс")
async def refresh_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] == "Скаут":
        collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow() - timedelta(
                                                minutes=1440)}})
        await message.answer("True")
    elif user_in_mongo["Essence"] == "Опустошитель":
        collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow() - timedelta(
                                                minutes=1440)}})
        await message.answer("True")
    elif user_in_mongo["Essence"] == "Штурмовик":
        collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow() - timedelta(
                                                minutes=1440)}})
        await message.answer("True")
    else:
        await message.answer("hui")


@bot.on.chat_message(text="Отправить корабль")
async def help_handler(message: Message):
    current = str(list(cruiser.find()))
    if str(message.from_id) in current:
        cruiser_id = cruiser.find_one({"_id": message.from_id})
        user_strength = cruiser_id["Strength"]
        aboba = random.choices(["win_self", "win_opp"], weights=[user_strength, enemy_list[cruiser_id["objective"]]["Strength"]], k=1)[0]
        if aboba == "win_self":
            rating_current = (3 / (
                        user_strength / (user_strength + enemy_list[cruiser_id["objective"]]["Strength"]))) * (enemy_list[cruiser_id["objective"]]["Strength"]/user_strength)
            collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow()}, "$inc": {"Experience": rating_current}})
            cruiser.delete_one({"_id": message.from_id})
            for i in range(len(cruiser_id["partners"])):
                collection.update_one({"_id": int(list(cruiser_id["partners"])[i])}, {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow()}, "$inc": {"Experience": 50}})
            await message.answer(message=f"Ваш отряд победил, каждый получил {rating_current} опыта")
        else:
            collection.update_one({"_id": message.from_id}, {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow()}, "$inc": {"Experience": 5}})
            await message.answer(message="Ваш отряд потерпел поражение, бонус 5 опыта")
            for i in range(len(cruiser_id["partners"])):
                collection.update_one({"_id": int(list(cruiser_id["partners"])[i])},
                                      {"$set": {"Dates.Date_ig_crusade.time": datetime.utcnow()},
                                       "$inc": {"Experience": 5}})
            cruiser.delete_one({"_id": message.from_id})
    else:
        await message.answer(message="У вас нет созданого ивента")


@bot.on.chat_message(text="Как играть")
async def reg_handler(message: Message):
    await message.answer(
        "Для того чтобы продолжить свое развитие в игровом боте:"
        "\n1)Проверьте доступные на данный момент планеты командой: Планеты"
        "\n2)Далее выберите нужную вам планету командой Рождение номер планеты(Пример: Рождение 1)"
        "\n3)Проверьте свой профиль командой: Статус"
        "\n4)Проверьте доступные вам команды: Доступные функции"
        "\np.s. О любых багах, несостыковоках и грамматических ошибках писать https://vk.com/id570495225")


@bot.on.chat_message(text=["Задачи", "задачи"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Essence"] in roles_imperium_ig:
        user_in_mongo = collection.find_one({"_id": message.from_id})["Dates"]
        count = 0
        for i in range(len(user_in_mongo)):
            count = count + 1
            name_dates = list(user_in_mongo)[count]
            await message.answer(
                f"{count}) {user_in_mongo[name_dates]['name']}")
    if user_in_mongo["Essence"] in roles_imperium_sm:
        user_in_mongo = collection.find_one({"_id": message.from_id})["Dates"]
        count = 0
        for i in range(len(user_in_mongo)):
            count = count + 1
            name_dates = list(user_in_mongo)[count]
            await message.answer(
                f"{count}) {user_in_mongo[name_dates]['name']}")


@bot.on.chat_message(text=("Дуэль <msg>"))
async def duel_handler(message: Message, msg):
    if "[id" in msg:
        id = int(msg.split("|")[0].replace("[id", ""))
        if message.from_id != id:
            user_in_mongo = collection.find_one({"_id": message.from_id})
            user_in_mongo2 = collection.find_one({"_id": id})
            if user_in_mongo["Planet"] == "Unknown":
                await message.answer(
                    message="Один из пользователей дуэли не рождён. Для списка планет введите команду: !Планеты, "
                            "а затем напишите команду: !Рождение Планета")
            elif user_in_mongo2["Planet"] == "Unknown":
                await message.answer(
                    message="Один из пользователей дуэли не рождён. Для списка планет введите команду: !Планеты, "
                            "а затем напишите команду: !Рождение Планета")
            elif user_in_mongo["Essence"] and user_in_mongo2["Essence"] in roles_imperium_ig:
                fight_logo = "Бой начался\n"
                aboba = random.choices(["win_self", "win_opp"], weights=[user_in_mongo["Strength"], user_in_mongo2["Strength"]], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (user_in_mongo["Strength"] + user_in_mongo2["Strength"]))) + 0.1
                    fight_logo = fight_logo + f"\nРезультат боя:\n [id{message.from_id}|{user_in_mongo['Nickname']}]: {user_in_mongo['Rating']} + {rating_current}\n[id{id}|{user_in_mongo2['Nickname']}] {user_in_mongo2['Rating']} + 0"
                    collection.update_one({'_id': message.from_id}, {'$inc': {'Rating': rating_current, 'Experience': rating_current}})
                    await message.answer(message=fight_logo)
                else:
                    rating_current = (1 / (user_in_mongo2["Strength"] / (user_in_mongo2["Strength"] + user_in_mongo["Strength"]))) + 0.1
                    fight_logo = fight_logo + f"\nРезультат боя:\n [id{id}|{user_in_mongo2['Nickname']}]: {user_in_mongo2['Rating']} + {rating_current}\n[id{message.from_id}|{user_in_mongo['Nickname']}] {user_in_mongo['Rating']} + 0"
                    collection.update_one({'_id': id}, {'$inc': {'Rating': rating_current, 'Experience': rating_current}})
                    await message.answer(message=fight_logo)
            elif user_in_mongo["Essence"] and user_in_mongo2["Essence"] in roles_imperium_sm:
                fight_logo = "Бой начался\n"
                aboba = random.choices(["win_self", "win_opp"], weights=[user_in_mongo["Strength"], user_in_mongo2["Strength"]], k=1)[0]
                if aboba == "win_self":
                    rating_current = (1 / (user_in_mongo["Strength"] / (user_in_mongo["Strength"] + user_in_mongo2["Strength"]))) + 0.1
                    fight_logo = fight_logo + f"\nРезультат боя:\n [id{message.from_id}|{user_in_mongo['Nickname']}]: {user_in_mongo['Rating']} + {rating_current}\n[id{id}|{user_in_mongo2['Nickname']}] {user_in_mongo2['Rating']} + 0"
                    collection.update_one({'_id': message.from_id}, {'$inc': {'Rating': rating_current, 'Experience': rating_current}})
                    await message.answer(message=fight_logo)
                else:
                    rating_current = (1 / (user_in_mongo2["Strength"] / (user_in_mongo2["Strength"] + user_in_mongo["Strength"]))) + 0.1
                    fight_logo = fight_logo + f"\nРезультат боя:\n [id{id}|{user_in_mongo2['Nickname']}]: {user_in_mongo2['Rating']} + {rating_current}\n[id{message.from_id}|{user_in_mongo['Nickname']}] {user_in_mongo['Rating']} + 0"
                    collection.update_one({'_id': id}, {'$inc': {'Rating': rating_current, 'Experience': rating_current}})
                    await message.answer(message=fight_logo)
            else:
                await message.answer(message=f"Один из дуэлянтов не имеет нужной роли")
        else:
            await message.answer(message="Нельзя сражатся с сами собой")
    else:
        await message.answer(message="Неизвестный пользователь")


@bot.on.chat_message(text="Как играть")
async def reg_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    await message.answer(
        f"[id{message.from_id}|{user_in_mongo['Nickname']}], для того чтобы продолжить свое развитие в игровом боте:"
        "\n1)Проверьте доступные на данный момент планеты командой: Планеты"
        "\n2)Далее выберите нужную вам планету командой Рождение номер планеты(Пример: Рождение 1)"
        "\n3)Проверьте свой профиль командой: Статус"
        "\n4)Проверьте доступные вам команды: Доступные функции"
        "\np.s. О любых багах, несостыковоках и грамматических ошибках писать https://vk.com/id570495225")


@bot.on.chat_message(text=["Доступные функции", "доступные функции", "Доступные команды", "доступные команды"])
async def info_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    if user_in_mongo["Planet"] == "Unknown":
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], для начала вам нужно выбрать планету")
    elif user_in_mongo["Essence"] in roles_imperium_ig:
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                             "1)Задачи - показывает доступные вам ивенты \n"
                             "2)Получить повышение - влить накопленный опыт в следующие звание \n"
                             "3)Поход - отправится в поход \n"
                             "4)Дуэль @пользователь - за победу в дуэли вы зарабатываете рейтинг и опыт")
    elif user_in_mongo["Essence"] in roles_imperium_sm:
        if user_in_mongo["Essence"] == "Кандидат":
            if user_in_mongo["implants"] in implants_0_5:
                await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                                     "1)Тренировка \n"
                                     "2)Химическая обработка\n"
                                     "3)Имплантация\n"
                                     "4)Подробнее (Информация об имплантации)")
            elif user_in_mongo["implants"] in implants_6_13:
                await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                                     "1)Тренировка \n"
                                     "2)Химическая обработка\n"
                                     "3)Гипнотерапия\n"
                                     "4)Имплантация\n"
                                     "5)Подробнее (Информация об имплантации)")
        elif user_in_mongo["Essence"] == "Неофит":
            await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                                 "1)Тренировка \n"
                                 "2)Стать скаутом")
        elif user_in_mongo["Essence"] == "Скаут":
            await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                                 "1)Тренировка \n"
                                 "2)Последняя имплантация\n"
                                 "3)Поход - отправится в поход")
        else:
            await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                                 "1)Задачи - показывает доступные вам ивенты \n"
                                 "2)Получить повышение - влить накопленный опыт в следующие звание \n"
                                 "3)Поход - отправится в поход \n"
                                 "4)Дуэль @пользователь - за победу в дуэли вы зарабатываете рейтинг и опыт")
    elif user_in_mongo["Planet"] == "Мир Улей":
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                             "1)Вступление ИГ - вступить в Имперскую Гвардию - 50 опыта\n"
                             "2)Работать - выполнять норму работы на вашей планете\n"
                             "3)Спуститься - список мест куда можно отправиться\n"
                             "4)Стать кандидатом - попытать удачу в вступлении в космодесант - 50 опыта, 50 силы")
    elif user_in_mongo["Planet"] == "Дикий Мир":
        await message.answer(f"[id{message.from_id}|{user_in_mongo['Nickname']}], доступные Вам команды:\n"
                             "1)Вступление ИГ - вступить в Имперскую Гвардию - 50 опыта\n"
                             "2)Охота - добывать пропитание\n"
                             "3)Арена - список оппонентов на арене\n"
                             "4)Стать кандидатом - попытать удачу в вступлении в космодесант - 50 опыта, 50 силы")
    else:
        await message.answer("Неизвестная ошибка")


@bot.on.chat_message(text=["Подробнее", "подробнее"])
async def give_handler(message: Message):
    user_in_mongo = collection.find_one({"_id": message.from_id})
    await message.answer(message=f"[id{message.from_id}|{user_in_mongo['Nickname']}], каждая имплантация стоит 50 опыта. Для успешной имплантации нужно поддерживать определенное кол-во силы. В случае, если начали имплантацию, не достигнув нужного кол-ва силы и она не удалась, ваша сила и опыт уменьшаться в 2 раза"
                                 f"\n1)Первая имплантация - 100% успех при 60 силы"
                                 f"\n2)Вторая имплантация - 100% успех при 70 силы"
                                 f"\n3)Третья имплантация - 100% успех при 80 силы"
                                 f"\n4)Четвертая имплантация - 100% успех при 90 силы"
                                 f"\n5)Пятая имплантация - 100% успех при 100 силы"
                                 f"\n6)Шестая имплантация - 100% успех при 120 силы"
                                 f"\n7)Седьмая имплантация - 100% успех при 150 силы")


@bot.on.chat_message(text=("Выдать <msg> <msg2>"))
async def give_handler(message: Message, msg, msg2):
    if message.from_id == 570495225:
        id = msg.split("|")[0].replace("[id", "")
        a = int(msg2)
        collection.update_one({'_id': int(id)}, {'$inc': {'Experience': int(a)}})
        await message.answer(message=f"True {msg}, {msg2}")


@bot.on.chat_message(text=("Снизить <msg> <msg2>"))
async def give_handler(message: Message, msg, msg2):
    if message.from_id == 570495225:
        id = msg.split("|")[0].replace("[id", "")
        a = int(msg2)
        collection.update_one({'_id': int(id)}, {'$inc': {'Experience': -int(a)}})
        await message.answer(message=f"True {msg}, {msg2}")


@bot.on.chat_message()
async def exp_handler(message: Message):
    collection.update_one({'_id': message.from_id}, {'$inc': {'Experience': 0.3}})


bot.run_forever()