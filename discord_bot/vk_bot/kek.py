import requests

def get_vk_token(username, password):
    # Параметры запроса
    params = {
        'grant_type': 'password',
        'client_id': '51732933',
        'client_secret': 'PLuowuSg2fv2KbcB1NQ0',
        'password': password,
        'username': username,
        'scope': '1073737727',
    }

    # Выполняем запрос на получение токена
    response = requests.post('https://oauth.vk.com/token', data=params)

    return response.text


if __name__ == '__main__':
    username = '+77478819863'
    password = '25071985ebdk'

    token = get_vk_token(username=username, password=password)
    print('Access Token:', token)
