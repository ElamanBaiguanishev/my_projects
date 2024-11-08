import requests
import json

url = "https://oauth.vk.com/authorize?client_id=51732933&redirect_uri=http://vkstandalone.pythonanywhere.com/&scope=notify,friends,photos,audio,video,docs,notes,pages,app_status,offline,notifications,wall,ads,offline,docs,pages,status,notes,offers,questions,wall,groups,email,notifications,stats,ads,offline,market&response_type=code&v=5.131"
response = requests.get(url)

if response.status_code == 200:
    print("Ответ:", response.text)
else:
    print("Произошла ошибка при отправке запроса:", response.status_code)

# https://oauth.vk.com/authorize?client_id=51732933&display=page&redirect_uri=http://vkstandalone.pythonanywhere.com/&scope=friends&response_type=code&v=5.131
# https://oauth.vk.com/authorize?client_id=51732933&redirect_uri=http://vkstandalone.pythonanywhere.com/&scope=notify,friends,photos,audio,video,docs,notes,pages,app_status,offline,notifications,wall,ads,offline,docs,pages,status,notes,offers,questions,wall,groups,email,notifications,stats,ads,offline,market&response_type=code&v=5.131
