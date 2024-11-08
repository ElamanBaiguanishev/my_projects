from speechkit import ShortAudioRecognition, Session

oauth_token = "y0_AgAAAABkj_sNAATuwQAAAADQQt1w-L-V1bwDRy-zTCvdEN4DHTY01TY"
catalog_id = "b1g6tv9g8fsuho2cbbuf"

# Экземпляр класса `Session` можно получать из разных данных
session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
# Читаем файл
with open('asd.wav', 'rb') as f:
    data = f.read()

# Создаем экземпляр класса с помощью `session` полученного ранее
recognizeShortAudio = ShortAudioRecognition(session)

# Передаем файл и его формат в метод `.recognize()`,
# который возвращает строку с текстом
text = recognizeShortAudio.recognize(
    data, format='lpcm', sampleRateHertz='8000')
print(text)