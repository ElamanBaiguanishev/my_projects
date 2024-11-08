from PIL import Image, ImageDraw


def make_background_transparent(input_image_path: Image) -> Image:
    # img = Image.open(input_image_path)
    img = input_image_path.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Превращаем все пиксели с белым фоном в прозрачные
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img


def resize_image(target_image: Image) -> Image:
    # Открываем изображения
    source_image = Image.open("main_say_this.png")

    # Получаем размеры исходного изображения
    source_width, source_height = source_image.size

    # Получаем размеры целевого изображения
    target_width, target_height = target_image.size

    # Вычисляем соотношение масштабирования
    scale_ratio = min(target_width / source_width, target_height / source_height)

    # Вычисляем новые размеры исходного изображения
    new_width = int(source_width * scale_ratio)
    new_height = int(source_height * scale_ratio)

    # Масштабируем изображение
    resized_image = source_image.resize((new_width, new_height), Image.LANCZOS)

    # Сохраняем масштабированное изображение
    return resized_image


def main(img: Image) -> Image:
    # Открываем изображение-фон
    background = img.convert("RGBA")

    # Открываем изображение, которое хотим наложить
    overlay = resize_image(background)

    width, height = overlay.size

    pixels = overlay.load()

    draw = ImageDraw.Draw(background)

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if pixel != (0, 0, 0, 0):
                draw.point((x, y), fill=(0, 0, 0, 0))

    return background


# main(Image.open("image (3).png")).save("result11.png")
