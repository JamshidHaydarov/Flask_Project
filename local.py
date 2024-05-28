import requests

# Примечание! Использовать только один запрос за раз.
# Пока пользуетесь одним запросом, другие запросы следут брать в коммент

# Отправляем GET запроса к нашему сайту
get_req = requests.get('http://127.0.0.1:5000/tasks/api')

# Отправляем POST запроса к нашему сайту
post_req = requests.post('http://127.0.0.1:5000/tasks/api', {'title' : "some title", "description": "some desc"})

# Отправка DELETE запроса к нашему сайту c id
del_req = requests.delete('http://127.0.0.1:5000/tasks/api/{id}')

# Отправляем PUT запрос к нашему сайту
put_req = requests.put('http://127.0.0.1:5000/tasks/api/{id}', {'title' : "some title", "description": "some desc"})



