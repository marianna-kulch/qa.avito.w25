import requests
from faker import Faker
import re

fake = Faker('ru_RU')
seller_id = 29032019 # Существующий sellerID
BASE_URL = "https://qa-internship.avito.com/api/1"  # URL сервиса

# Создание корректного тестового обьявления
def create_correct_item():
    name = fake.name()
    price = fake.random_int(min=0, max=100_000)
    statistics_contacts = fake.random_int(min=0, max=100)
    statistics_likes = fake.random_int(min=0, max=100)
    statistics_view_count = fake.random_int(min=0, max=100)

    data = {
        "name": name,
        "price": price,
        "sellerID": seller_id,
        "statistics": {
            "contacts": statistics_contacts,
            "likes": statistics_likes,
            "viewCount": statistics_view_count
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    item_data = response.json()
    uuid_regex = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'  # Регулярное выражение для UUID
    match = re.search(uuid_regex, item_data["status"])

    item_id = match.group(1)
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    assert response.status_code == 200  # Проверяем успешный запрос
    item_data = response.json()

    return item_data[0]

# Тест на создание объявления с валидными данными
def test_create_item_success():
    name = fake.name()
    price = fake.random_int(min=0, max=100_000)
    statistics_contacts = fake.random_int(min=0, max=100)
    statistics_likes = fake.random_int(min=0, max=100)
    statistics_view_count = fake.random_int(min=0, max=100)

    data = {
        "name": name,
        "price": price,
        "sellerID": seller_id,
        "statistics": {
            "contacts": statistics_contacts,
            "likes": statistics_likes,
            "viewCount": statistics_view_count
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code == 200  # Проверяем, что код ответа 200
    item_data = response.json()
    uuid_regex = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})' # Регулярное выражение для UUID

    match = re.search(uuid_regex, item_data["status"])
    assert re.search(uuid_regex, item_data["status"]) # Убедимся, что есть уникальный ID объявления

    # Если найдено совпадение, извлечь значение
    if match:
        item_id = match.group(1)
        response = requests.get(f"{BASE_URL}/item/{item_id}")
        assert response.status_code == 200  # Проверяем успешный запрос
        item_data = response.json()
        assert item_data[0]["id"] == item_id  # Проверим уникальный ID объявления
        assert item_data[0]["name"] == name  # Проверим корректность поля name сохраненного объявления
        assert item_data[0]["price"] == price  # Проверим корректность поля price сохраненного объявления
        assert item_data[0]["sellerId"] == seller_id  # Проверим корректность поля sellerId сохраненного объявления
        assert item_data[0]["statistics"]["contacts"] == statistics_contacts  # Проверим корректность поля contacts сохраненного объявления
        assert item_data[0]["statistics"]["likes"] == statistics_likes  # Проверим корректность поля likes сохраненного объявления
        assert item_data[0]["statistics"]["viewCount"] == statistics_view_count  # Проверим корректность поля viewCount сохраненного объявления

# Тест для отправки запроса с пустым значением поля name
def test_create_item_empty_name():
    name = ""
    price = fake.random_int(min=1, max=100_000)
    statistics_contacts = fake.random_int(min=0, max=100)
    statistics_likes = fake.random_int(min=0, max=100)
    statistics_view_count = fake.random_int(min=0, max=100)

    data = {
        "name": name, # Пустая строка
        "price": price,
        "sellerID": seller_id,
        "statistics": {
            "contacts": statistics_contacts,
            "likes": statistics_likes,
            "viewCount": statistics_view_count
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code == 400 # Ожидаем код 400 (Bad Request)
    message = response.json()
    assert message["status"] == "400"  # Проверим статус ошибки
    assert message["result"]["message"] == "переданы некорректные данные"  # Проверим сообщение об ошибке

# Тест на создание объявления с некорректным типом данных
def test_create_item_invalid_price():
    name = fake.name()
    invalid_price = fake.businesses_inn()
    statistics_contacts = fake.random_int(min=0, max=100)
    statistics_likes = fake.random_int(min=0, max=100)
    statistics_view_count = fake.random_int(min=0, max=100)

    data = {
        "name": name,
        "price": invalid_price, # Неверный тип данных для цены
        "sellerID": seller_id,
        "statistics": {
            "contacts": statistics_contacts,
            "like": statistics_likes,
            "viewCount": statistics_view_count
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code in [400,500]  # Ожидаемый код ошибки
    message = response.json()
    assert message["status"] in ["400","500"]  # Проверим статус ошибки
    assert message["result"]["message"] == "не передано тело объявления"  # Проверим сообщение об ошибке

# Тест на создание объявления с отрицательным значением для sellerID
def test_create_item_neg_seller_id():
    neg_seller_id = -1
    name = fake.name()
    price = fake.random_int(min=0, max=10_000)
    statistics_contacts = fake.random_int(min=0, max=100)
    statistics_likes = fake.random_int(min=0, max=100)
    statistics_view_count = fake.random_int(min=0, max=100)

    data = {
        "name": name,
        "price": price,
        "sellerID": neg_seller_id,
        "statistics": {
            "contacts": statistics_contacts,
            "like": statistics_likes,
            "viewCount": statistics_view_count
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code in [400,500]  # Ожидаемый код ошибки
    message = response.json()
    assert message["status"] in ["400","500"]  # Проверим статус ошибки
    assert message["result"]["message"] == "передан некорректный идентификатор продавца" # Проверим сообщение об ошибке

# Тест на создание объявления с отсутствием обязательного поля
def test_create_item_missing_fields():
    price = fake.random_int(min=1000, max=100_000)

    data = {
        "price": price,
        "sellerID": seller_id
    }
    response = requests.post(f"{BASE_URL}/item", json=data)
    assert response.status_code in [400,500]  # Ожидаемый код ошибки
    message = response.json()
    assert message["status"] in ["400","500"]  # Проверим статус ошибки
    assert message["result"]["message"] == "не передано тело объявления"  # Проверим сообщение об ошибке

# Тест для отправки запроса с отрицательным значением поля price
def test_create_item_negative_price():
    name = fake.name()
    invalid_price = fake.random_int(min=-100_000, max=-1)
    statistics_contacts = fake.random_int(min=0, max=100)
    statistics_likes = fake.random_int(min=0, max=100)
    statistics_view_count = fake.random_int(min=0, max=100)

    data = {
        "name": name,
        "price": invalid_price, # Некорректное отрицательное значение
        "sellerID": seller_id,
        "statistics": {
            "contacts": statistics_contacts,
            "like": statistics_likes,
            "viewCount": statistics_view_count
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
    response = requests.get(f"{BASE_URL}/{seller_id}/item")
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
