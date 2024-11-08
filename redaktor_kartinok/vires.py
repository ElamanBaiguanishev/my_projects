import json

from PIL import Image, ImageDraw

from main import resize_image

new_image = Image.open("image (3).png").convert("RGBA")
# Открываем изображение
image = resize_image(new_image)

# Получаем ширину и высоту изображения
width, height = image.size

# Получаем объект изображения для доступа к пикселям
pixels = image.load()

# Список для сохранения координат
transparent_pixels = []

# Проходим через каждый пиксель и сохраняем координаты, где цвет полностью прозрачный (0, 0, 0, 0)
for y in range(height):
    for x in range(width):
        pixel = pixels[x, y]
        if pixel != (0, 0, 0, 0):
            transparent_pixels.append((x, y))

draw = ImageDraw.Draw(new_image)

for coord in transparent_pixels:
    x, y = coord
    draw.point((x, y), fill=(0, 0, 0, 0))

# Сохраняем результат
new_image.save("output_image.png")
