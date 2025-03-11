import requests
from flask import Flask
from waitress import serve


def get_credentials() -> dict[str, str]:
    credentials = {'unifi_url': '',
                   'username': '',
                   'password': ''}
    try:
        for key in credentials.keys():
            with open('credentials.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if key in line:
                        credentials[key] = line.split('=')[1]
                        break
        return credentials
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def get_clients():
    # Получаем данные для авторизации из файла
    credentials = get_credentials()

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
        'username': credentials['username'],
        'password': credentials['password']
    }

    login_url = f'{credentials['unifi_url']}/api/login'
    response = session.post(login_url, json=login_payload, headers=headers)

    # Проверяем успешность входа
    if response.status_code != 200:
        print(f"Ошибка входа: {response.status_code}")
        exit()

    # Получаем информацию о подключенных клиентах
    clients_url = f'{credentials['unifi_url']}/api/s/default/stat/sta'
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
    serve(app, host='0.0.0.0', port=5003)

# docker-compose up -d --build
