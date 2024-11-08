import requests
import time
apiurl = 'https://api.vk.com/method/'
token = 'token'
chatid = 1
text = 'жопаписька'

while True:
	one = requests.get(apiurl + 'messages.send', {'v': 5.67, 'access_token': token, 'chat_id': 
			chatid, 'message': 'a'})
	two = requests.get(apiurl + 'messages.edit', {'v': 5.67, 'access_token': token, 'peer_id': 
			2000000000 + chatid, 'message_id': one.json()['response'], 'message': text})
	print(two.json())
	time.sleep(7)