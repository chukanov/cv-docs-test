# Запуск тестов CV-docs
## Подготовка окружения
### Установите Python

Если у вас еще нет Python 3.9+, скачайте и установите его:
[Python](https://www.python.org/downloads/windows/)

Во время установки обязательно поставьте галочку:
✅ “Add Python to PATH”

Проверьте установку, запустив в командной строке (cmd):

```commandline
python --version
```

### Подготовка структуры папок и файлов
Перед запуском теста убедитесь, что у вас правильно организована структура директорий:
```
📁 test_data
   ├── 📁 Иванова Екатерина Ивановна
   │   ├── p.jpg  # Паспорт
   │   ├── d.jpeg # Диплом
   │   ├── s.png  # Свидетельство о браке (если есть)
   ├── 📁 Петрова Антонина Сергеевна
   │   ├── p.png
   │   ├── d.pdf
   │   ├── s.jpeg
   ├── 📄 test.csv  # Данные для тестирования       
📄 test.py  # Тестовый скрипт
```
т.е. папка с данными пользователей должна находиться рядом с файлом test.py.
**Очень важно:** для каждого пользователя файлы с паспортом, дипломом и свидетельством о браке должны называться соответвенно p, d, s.

###  Описание xlsx-файла test.xslx
CSV-файл test.csv содержит данные для тестирования API. Он расположен в папке test_data и имеет следующую структуру:
Каждая строка в файле описывает одного человека, чьи документы будут проверяться сервисом.

Колонки:

| Колонка | Тип | Обязательность | Описание |
|---|---|---|---|
| lastName | str | ✅ Да | Фамилия владельца документов |
| firstName | str | ✅ Да | Имя владельца документов |
| surName | str | ✅ Да | Отчество владельца документов |
| gender | str | ✅ Да | Пол (допустимые значения: Male, Female) |
| birthDate | str | ✅ Да | Дата рождения в формате YYYY-MM-DD |
| diplomaCountry | str | ✅ Да | Страна, в которой был выдан диплом |
| educationLevel | str | ✅ Да | Уровень образования (Высшее образование, Среднее профессиональное образование) |
| diplomaLastName | str | ✅ Да | Фамилия после брака  |

Пример:
```csv
lastName;firstName;surName;gender;birthDate;diplomaCountry;educationLevel;diplomaLastName
Иванова;Екатерина;Ивановна;Female;1990-01-01;Россия;Высшее образование;Петрова
Петров;Алексей;Сергеевич;Male;1985-05-23;Казахстан;Среднее профессиональное образование;Петров
Сидоров;Максим;Игоревич;Male;1992-12-15;Беларусь;Высшее образование;Сидоров
```

### Установка библиотек
Тестовый скрипт использует несколько стандартных библиотек Python, но одна (requests) может отсутствовать в системе.
Чтобы ее установить, выполните в командной строке:
```commandline
pip install requests
pip install openpyxl
```

### Настройка теста
Все параметры тестирования задаются непосредственно в Python-файле (test.py).
Перед запуском убедитесь, что настроены следующие параметры:
```python

# === Настройки теста ===
TEST_DATA_DIR = "test_data"  # Папка с тестовыми данными
CSV_FILE = os.path.join(TEST_DATA_DIR, "test.xslx")  # Путь к CSV-файлу
API_URL = "http://localhost:8000/v1/verifyStudentsData"  # Адрес API сервиса
RESULTS_FILE = "test_results.csv"  # Файл для записи результатов тестов
AUTH_TOKEN = "02cf6d4e-b8fa"  # Токен авторизации 
```

Если необходимо изменить путь к данным или API, просто исправьте значения в этом файле.


### Запуск теста
Откройте командную строку (PowerShell или cmd.exe) и перейдите в папку, где находится test.py.
Запустите тест с помощью команды:
```commandline
python test_service.py
```


