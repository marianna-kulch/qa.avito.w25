import requests
from faker import Faker
import re

fake = Faker('ru_RU')
SELLER_ID = 29032019 # Существующий sellerID
BASE_URL = "https://qa-internship.avito.com/api/1"  # URL сервиса
UUID_REGEX = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'  # Регулярное выражение для UUID

def give_me_fake_data():
    return {
        "name": fake.name(),
        "price": fake.random_int(min=1, max=100_000),
        "sellerID": SELLER_ID,
        "statistics": {
            "contacts": fake.random_int(min=0, max=100),
            "likes": fake.random_int(min=0, max=100),
            "viewCount": fake.random_int(min=0, max=100)
        }
    }

# Создание корректного тестового обьявления
def create_correct_item():
    fake_data = give_me_fake_data()

    data = {
        "name": fake_data['name'],
        "price": fake_data['price'],
        "sellerID": fake_data['sellerID'],
        "statistics": {
            "contacts": fake_data['statistics']['contacts'],
            "likes": fake_data['statistics']['likes'],
            "viewCount": fake_data['statistics']['viewCount']
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    item_data = response.json()
    match = re.search(UUID_REGEX, item_data["status"])

    item_id = match.group(1)
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    assert response.status_code == 200  # Проверяем успешный запрос
    item_data = response.json()

    return item_data[0]

# Тест на создание объявления с валидными данными
def test_create_item_success():
    fake_data = give_me_fake_data()

    data = {
        "name": fake_data['name'],
        "price": fake_data['price'],
        "sellerID": fake_data['sellerID'],
        "statistics": {
            "contacts": fake_data['statistics']['contacts'],
            "likes": fake_data['statistics']['likes'],
            "viewCount": fake_data['statistics']['viewCount']
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code == 200  # Проверяем, что код ответа 200
    item_data = response.json()

    match = re.search(UUID_REGEX, item_data["status"])
    assert match # Убедимся, что есть уникальный ID объявления

    # Если найдено совпадение, извлечь значение
    if match:
        item_id = match.group(1)
        response = requests.get(f"{BASE_URL}/item/{item_id}")
        assert response.status_code == 200  # Проверяем успешный запрос
        item_data = response.json()
        assert item_data[0]["id"] == item_id  # Проверим уникальный ID объявления
        assert item_data[0]["name"] == fake_data['name']  # Проверим корректность поля name сохраненного объявления
        assert item_data[0]["price"] == fake_data['price']  # Проверим корректность поля price сохраненного объявления
        assert item_data[0]["sellerId"] == fake_data['sellerID']  # Проверим корректность поля sellerId сохраненного объявления
        assert item_data[0]["statistics"]["contacts"] == fake_data['statistics']['contacts']  # Проверим корректность поля contacts сохраненного объявления
        assert item_data[0]["statistics"]["likes"] == fake_data['statistics']['likes']  # Проверим корректность поля likes сохраненного объявления
        assert item_data[0]["statistics"]["viewCount"] == fake_data['statistics']['viewCount']  # Проверим корректность поля viewCount сохраненного объявления

# Тест для отправки запроса с пустым значением поля name
def test_create_item_empty_name():
    fake_data = give_me_fake_data()

    data = {
        "name": "", # Пустая строка
        "price": fake_data['price'],
        "sellerID": fake_data['sellerID'],
        "statistics": {
            "contacts": fake_data['statistics']['contacts'],
            "likes": fake_data['statistics']['likes'],
            "viewCount": fake_data['statistics']['viewCount']
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code == 400 # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] == "400"  # Проверим статус ошибки
    assert message["result"]["message"] == "переданы некорректные данные"  # Проверим сообщение об ошибке

# Тест на создание объявления с некорректным типом данных
def test_create_item_invalid_price():
    fake_data = give_me_fake_data()

    data = {
        "name": fake_data['name'],
        "price": fake.name(), # Неверный тип данных для цены
        "sellerID": fake_data['sellerID'],
        "statistics": {
            "contacts": fake_data['statistics']['contacts'],
            "likes": fake_data['statistics']['likes'],
            "viewCount": fake_data['statistics']['viewCount']
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code in [400,500]  # Ожидаемый код ошибки
    message = response.json()
    assert message["status"] in ["400","500"]  # Проверим статус ошибки
    assert message["result"]["message"] == "не передано тело объявления"  # Проверим сообщение об ошибке

# Тест на создание объявления с отрицательным значением для sellerID
def test_create_item_neg_seller_id():
    fake_data = give_me_fake_data()

    data = {
        "name": fake_data['name'],
        "price": fake_data['price'],
        "sellerID": -1, # Отрицательное значение для sellerID
        "statistics": {
            "contacts": fake_data['statistics']['contacts'],
            "likes": fake_data['statistics']['likes'],
            "viewCount": fake_data['statistics']['viewCount']
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code in [400,500]  # Ожидаемый код ошибки
    message = response.json()
    assert message["status"] in ["400","500"]  # Проверим статус ошибки
    assert message["result"]["message"] == "передан некорректный идентификатор продавца" # Проверим сообщение об ошибке

# Тест на создание объявления с отсутствием обязательного поля
def test_create_item_missing_fields():
    fake_data = give_me_fake_data()

    data = {
        "price": fake_data['price'],
        "sellerID": fake_data['sellerID']
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code in [400,500]  # Ожидаемый код ошибки
    message = response.json()
    assert message["status"] in ["400","500"]  # Проверим статус ошибки
    assert message["result"]["message"] == "не передано тело объявления"  # Проверим сообщение об ошибке

# Тест для отправки запроса с отрицательным значением поля price
def test_create_item_negative_price():
    fake_data = give_me_fake_data()

    data = {
        "name": fake_data['name'],
        "price": fake.random_int(min=-100_000, max=-1),
        "sellerID": fake_data['sellerID'],
        "statistics": {
            "contacts": fake_data['statistics']['contacts'],
            "likes": fake_data['statistics']['likes'],
            "viewCount": fake_data['statistics']['viewCount']
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code == 400  # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] == "400" # Проверим статус ошибки
    assert message["result"]["message"] == "переданы некорректные данные"  # Проверим сообщение об ошибке

# Тест на получение объявления по валидному ID
def test_get_item_by_valid_id():
    item = create_correct_item()  # ID созданного обьявления
    response = requests.get(f"{BASE_URL}/item/{item['id']}")
    assert response.status_code == 200  # Проверяем успешный запрос
    item_data = response.json()
    assert item_data[0]["id"] == item["id"] # Убедимся, что получили верное объявление

# Тест на получение объявления по несуществующему ID
def test_get_item_by_invalid_id():
    item_id = "bfb5d90f-b8c7-4585-8a88-0bb1771cf000"  # Несуществующий ID
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    assert response.status_code == 404  # Ожидаем код 404 Not Found
    message = response.json()
    assert message["status"] == "404" # Проверим статус ошибки
    assert message["result"]["message"] == "item " + item_id + " not found"  # Проверим сообщение об ошибке

# Тест на получение объявления по некорректному ID
def test_get_item_by_incorrect_id():
    item_id = fake.name() # Некорректный ID
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    assert response.status_code in [400,404]  # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] in ["400","404"]  # Проверим статус ошибки
    assert message["result"]["message"] == "передан некорректный идентификатор объявления"  # Проверим сообщение об ошибке

# Тест на получение всех объявлений по валидному sellerID
def test_get_items_by_seller_id():
    response = requests.get(f"{BASE_URL}/{SELLER_ID}/item")
    assert response.status_code == 200  # Проверяем успешный запрос
    item_list_data = response.json()
    assert isinstance(item_list_data, list)  # Проверяем, что вернулся список объявлений

# Тест на получение объявлений для несуществующего sellerID
def test_get_items_by_invalid_seller_id():
    seller_id = 123456789  # Несуществующий sellerID
    response = requests.get(f"{BASE_URL}/{seller_id}/item")
    assert response.status_code == 200  # Сервис должен вернуть успешный ответ
    item_list_data = response.json()
    assert len(item_list_data) == 0  # Ожидаем пустой список

# Тест на получение объявлений для sellerID с отрицательным значением
def test_get_items_by_negative_seller_id():
    seller_id = fake.random_int(min=-100_000, max=-1)  # Некорректный sellerID
    response = requests.get(f"{BASE_URL}/{seller_id}/item")
    assert response.status_code == 400  # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] == "400"  # Проверим статус ошибки
    assert message["result"]["message"] == "передан некорректный идентификатор продавца"  # Проверим сообщение об ошибке

# Тест на получение объявлений для некорректного типа данных sellerID
def test_get_items_by_incorrect_type_seller_id():
    seller_id = fake.name() # Некорректный тип данных sellerID
    response = requests.get(f"{BASE_URL}/{seller_id}/item")
    assert response.status_code == 400  # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] == "400" # Проверим статус ошибки
    assert message["result"]["message"] == "передан некорректный идентификатор продавца"  # Проверим сообщение об ошибке

# Тест на получение статистики по существующему itemID
def test_get_statistic_by_item_id():
    item = create_correct_item()  # ID созданного обьявления
    response = requests.get(f"{BASE_URL}/statistic/{item['id']}")
    assert response.status_code == 200  # Сервис должен вернуть успешный ответ
    item_data = response.json()
    assert item_data[0]["contacts"] == item["statistics"]["contacts"]  # Проверим контакты
    assert item_data[0]["likes"] == item["statistics"]["likes"]  # Проверим лайки
    assert item_data[0]["viewCount"] == item["statistics"]["viewCount"]  # Проверим просмотры

# Тест на получение статистики по несуществующему itemID
def test_get_statistic_by_invalid_item_id():
    itemID = "f000abd0-c000-00de-0ea0-00e000a00000" # Несуществующий itemID
    response = requests.get(f"{BASE_URL}/statistic/{itemID}")
    assert response.status_code == 404  # Ожидаем код 404 Not Found
    message = response.json()
    assert message["status"] == "404"  # Проверим статус ошибки
    assert message["result"]["message"] == "statistic " + itemID + " not found"  # Проверим сообщение об ошибке

# Тест на получение статистики по некорректному itemID
def test_get_statistic_by_incorrect_item_id():
    itemID = fake.name() # Некорректный ID
    response = requests.get(f"{BASE_URL}/statistic/{itemID}")
    assert response.status_code in [400,404]  # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] in ["400","404"]  # Проверим статус ошибки
    assert message["result"]["message"] == "передан некорректный идентификатор объявления"  # Проверим сообщение об ошибке
