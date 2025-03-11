import requests
from flask import Flask

# Данные для аутентификации
unifi_url = ''
username = ''
password = ''


def get_clients():


    # Создаем сессию для сохранения cookies
    session = requests.Session()

    # Устанавливаем заголовки
    headers = {
        'Content-Type': 'application/json'
    }

    # Отключаем проверку SSL-сертификатов (если используете самоподписанный сертификат)
    session.verify = False

    # Логинимся в UniFi Controller
    login_payload = {
        'username': username,
        'password': password
    }

    login_url = f'{unifi_url}/api/login'
    response = session.post(login_url, json=login_payload, headers=headers)

    # Проверяем успешность входа
    if response.status_code != 200:
        print(f"Ошибка входа: {response.status_code}")
        exit()

    # Получаем информацию о подключенных клиентах
    clients_url = f'{unifi_url}/api/s/default/stat/sta'
    clients_response = session.get(clients_url, headers=headers)
    # Закрываем сессию
    session.close()

    # Проверяем успешность запросов
    if clients_response.status_code == 200:
        return clients_response.json()['data']
    else:
        return f'Ошибка запроса по клиентам: {clients_response.status_code}'



# Создаем Flask приложение
app = Flask(__name__)

# Маршрут для получения данных о подключенных клиентах
@app.route('/unifi/get_clients', methods=['GET'])
def unifi_get_clients():
    return get_clients()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
