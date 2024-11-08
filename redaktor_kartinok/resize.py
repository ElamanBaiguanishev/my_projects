from PIL import Image


def resize_image(target_img) -> Image:
    # Открываем изображения
    source_image = Image.open("main_say_this.png")
    target_image = Image.open(target_img)

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

# resize_image("main_say_this.png", "eris.png")
