from fuzzywuzzy import fuzz, process


def approximate(answers_dict, answer):
    best_match, score = process.extractOne(answer, answers_dict.keys(), scorer=fuzz.ratio)

    if score >= 80:
        value = answers_dict[best_match]
        return value


def find_most_similar_answer(correct_answer, answer_choices):
    # Инициализируем переменные для хранения наиболее схожего ответа и его схожности
    most_similar_answer = None
    highest_similarity = 0
    threshold = 50

    # Проходим по всем вариантам ответов
    for answer in answer_choices:
        # Используем функцию fuzz.ratio для определения схожести (от 0 до 100)
        similarity = fuzz.ratio(correct_answer, answer)

        # Если текущий ответ более схож с правильным, чем наиболее схожий найденный ответ,
        # обновляем наиболее схожий ответ и его схожность
        if similarity > highest_similarity:
            most_similar_answer = answer
            highest_similarity = similarity

    # Проверяем, схож ли наиболее схожий ответ с порогом
    if highest_similarity >= threshold:
        return most_similar_answer
    else:
        return None
