import cv2
import pytesseract


# Указываем путь к Tesseract OCR (если он не находится в стандартной директории)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR/tesseract'


def find_word_coordinates(image_path, word):
    # Загрузка изображения с помощью OpenCV
    image = cv2.imread(image_path)

    # Конвертируем изображение в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем бинаризацию для упрощения обработки
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Используем pytesseract для распознавания текста на изображении
    data = pytesseract.image_to_data(binary_image, output_type=pytesseract.Output.DICT, lang="rus")

    # Находим координаты слова и центр квадрата
    word_coordinates = []
    square_centers = []
    for i in range(len(data['text'])):
        if data['text'][i] == word:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            word_coordinates.append((x, y, x + w, y + h))
            center_x = x + w // 2
            center_y = y + h // 2
            square_centers.append((center_x, center_y))

    # Создаем копию изображения и рисуем прямоугольник вокруг слова и кружок в центре квадрата
    image_with_shapes = image.copy()
    for (x_start, y_start, x_end, y_end), (center_x, center_y) in zip(word_coordinates, square_centers):
        cv2.rectangle(image_with_shapes, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.circle(image_with_shapes, (center_x, center_y), 5, (0, 0, 255), -1)

    print(square_centers)

    return image_with_shapes


if __name__ == "__main__":
    image_path = "img_1.png"
    word_to_find = "изменение"
    result_image = find_word_coordinates("img_2.png", "Подождите")

    # Сохраняем результат в новый файл
    cv2.imwrite("result.jpg", result_image)
