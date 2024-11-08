import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def coord(image_path, target_sentence, language='rus'):
    data = pytesseract.image_to_data(image_path, lang=language, output_type=pytesseract.Output.DICT)
    for i, text in enumerate(data['text']):
        if target_sentence in text:
            x, y = data['left'][i], data['top'][i]
            print("Нашел")
            return x, y

    return None


def coord_eng(image_path, target_sentence, language='eng'):
    data = pytesseract.image_to_data(image_path, lang=language, output_type=pytesseract.Output.DICT)
    for i, text in enumerate(data['text']):
        if target_sentence in text:
            x, y = data['left'][i], data['top'][i]
            print("Нашел")
            return x, y

    return None
