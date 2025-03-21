# API Тестирование микросервиса объявлений

Этот проект автоматизирует тестирование API микросервиса объявлений с использованием Python и pytest.

**Описание сервиса:**

Сервис умеет хранить данные по объявлениям, сохранять и получать все объявления по пользователю. Каждое созданное объявление имеет уникальный идентификатор, остальные поля могут быть неуникальными.

## Установка и запуск

### 1. Клонируйте репозиторий:
Выполните команду в терминале:
```bash
git clone git@github.com:marianna-kulch/qa.avito.w25.git
```
Либо скачайте ZIP-архив проекта по ссылке и распакуйте его.

### 2. Проверьте установку Python:

Убедитесь, что на вашем компьютере установлен Python. Выполните команду в командной строке/терминале:
```bash
python --version
```

Если Python не установлен, скачайте его с официального сайта и установите, отметив опцию "Add python.exe to PATH" во время установки.

### 3. Перейдите в директорию проекта:

В терминале выполните команду для перехода в корневую директорию проекта:
```bash
cd ./qa.avito.w25/task2
```

### 4. Установите зависимости:

Выполните команду для установки необходимых библиотек:
```bash
pip install -r requirements.txt
```

### 5. Запустите автотесты:

Чтобы запустить тесты, выполните команду:
```bash
pytest test_avito.py
```
