import random
import string


def generate_random_string():
    return ''.join(random.choices(string.ascii_letters, k=8))


def generate_mock_list():
    return [generate_random_string() for i in range(30)]


data = {
    "Семестр 1": {"слово1_1": generate_mock_list(), "слово1_2": generate_mock_list(),
                  "слово1_3": generate_mock_list(), "слово1_4": generate_mock_list(),
                  "слово1_5": generate_mock_list()},
    "Семестр 2": {"слово2_1": generate_mock_list(), "слово2_2": generate_mock_list(),
                  "слово2_3": generate_mock_list(), "слово2_4": generate_mock_list(),
                  "слово2_5": generate_mock_list()},
    "Семестр 3": {"слово3_1": generate_mock_list(), "слово3_2": generate_mock_list(),
                  "слово3_3": generate_mock_list(), "слово3_4": generate_mock_list(),
                  "слово3_5": generate_mock_list()},
    "Семестр 4": {"слово4_1": generate_mock_list(), "слово4_2": generate_mock_list(),
                  "слово4_3": generate_mock_list(), "слово4_4": generate_mock_list(),
                  "слово4_5": generate_mock_list()},
    "Семестр 5": {"слово5_1": generate_mock_list(), "слово5_2": generate_mock_list(),
                  "слово5_3": generate_mock_list(), "слово5_4": generate_mock_list(),
                  "слово5_5": generate_mock_list()},
    "Семестр 6": {"слово6_1": generate_mock_list(), "слово6_2": generate_mock_list(),
                  "слово6_3": generate_mock_list(), "слово6_4": generate_mock_list(),
                  "слово6_5": generate_mock_list()}
}

print(data)
