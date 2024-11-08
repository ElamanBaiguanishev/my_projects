from telethon.sync import TelegramClient

api_id = 28783220
api_hash = '414a612d67c5aa5d665c09a3ec0eec5b'
session_name = '+79658783530.session'

client = TelegramClient(session_name, api_id, api_hash)
client.start()
