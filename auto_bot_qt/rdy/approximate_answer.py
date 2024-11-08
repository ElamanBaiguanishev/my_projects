from fuzzywuzzy import fuzz, process


def approximate(answers_dict, answer):
    best_match, score = process.extractOne(answer, answers_dict.keys(), scorer=fuzz.ratio)

    if score >= 80:
        value = answers_dict[best_match]
        return value
