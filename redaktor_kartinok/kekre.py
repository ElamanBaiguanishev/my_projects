from PIL import Image

# Открываем изображение-фон
background = Image.open("eris.png")

# Открываем изображение, которое хотим наложить
overlay = Image.open("main_say_this.png")

# Наложение изображения на фон
background.paste(overlay, (0, 0), overlay)

# Сохраняем результат в формате PNG
background.save("result.png")
