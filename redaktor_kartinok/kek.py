from PIL import Image, ImageDraw

# Открываем изображение
image = Image.open("main_say_this.png")

# Получаем данные о размерах изображения
width, height = image.size

# Создаем объект ImageDraw для рисования на изображении
draw = ImageDraw.Draw(image)

# Итерируем по каждому пикселю изображения
for x in range(width):
    for y in range(height):
        # Получаем цвет пикселя
        pixel_color = image.getpixel((x, y))

        # Проверяем альфа-канал (прозрачность)
        if len(pixel_color) == 4 and pixel_color[3] != 0:
            # Заменяем непрозрачный пиксель на белый цвет
            draw.point((x, y), fill="white")

# Сохраняем измененное изображение
image.save("main_say_this.png")
