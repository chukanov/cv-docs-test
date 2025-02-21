import os
import csv
import base64
import requests
import json

# === Настройки ===
TEST_DATA_DIR = "test_data"  # Папка с тестовыми данными
CSV_FILE = os.path.join(TEST_DATA_DIR, "test.csv")  # Путь к CSV
API_URL = "http://localhost:8000/v1/verifyStudentsData"  # Адрес API
RESULTS_FILE = "test_results.csv"  # Файл для записи результатов тестов
AUTH_TOKEN = "16dg8a8s-d4tx"

# === Функция кодирования файла в Base64 ===
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# === Определение MIME-типа по расширению ===
MIME_TYPES = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "pdf": "application/pdf"
}

def get_mime_type(filename):
    ext = filename.split(".")[-1].lower()
    return MIME_TYPES.get(ext, "application/octet-stream")

# === Чтение CSV ===
with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    test_results = []

    for row in reader:
        last_name = row["lastName"]
        first_name = row["firstName"]
        sur_name = row["surName"]
        gender = row["gender"]
        birth_date = row["birthDate"]
        diploma_country = row["diplomaCountry"]
        education_level = row["educationLevel"]
        diploma_last_name = row.get("diplomaLastName", "")

        # Определяем путь к папке владельца
        user_folder = os.path.join(TEST_DATA_DIR, f"{last_name} {first_name} {sur_name}")

        # Проверяем наличие папки
        if not os.path.isdir(user_folder):
            print(f"⚠️ Папка {user_folder} не найдена. Пропускаем.")
            continue

        # Ищем файлы паспорта, диплома и свидетельства о браке
        user_files = {}
        for file_type, file_prefix in {"passport": "p", "diploma": "d", "marriageCertificate": "s"}.items():
            for ext in MIME_TYPES.keys():
                file_path = os.path.join(user_folder, f"{file_prefix}.{ext}")
                if os.path.exists(file_path):
                    user_files[file_type] = {
                        "fileName": os.path.basename(file_path),
                        "mimeType": get_mime_type(file_path),
                        "data": encode_file_to_base64(file_path)
                    }
                    break  # Нашли файл, больше не ищем
            else:
                if file_type != "marriageCertificate":  # Свидетельство о браке не обязательно
                    print(f"⚠️ Файл {file_prefix} не найден в {user_folder}. Пропускаем.")
                    continue

        # Формируем JSON-запрос
        payload = {
            "userInfo": {
                "firstName": first_name,
                "surName": sur_name,
                "lastName": last_name,
                "gender": gender,
                "birthDate": birth_date,
                "diplomaCountry": diploma_country,
                "educationLevel": education_level,
                "diplomaLastName": diploma_last_name
            },
            "userFiles": user_files
        }

        # Заголовки запроса с авторизацией
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        # Отправка запроса
        try:
            response = requests.post(API_URL, json=payload, timeout=30, headers=headers)
            response_json = response.json()
            status = response_json.get("status", "error")
            if status=="success":
                result = "✅ Passed"
            else:
                result = "❌ Failed ({raw_resp})"
        except Exception as e:
            result = f"❌ Failed response: {str(e)}"

        # Логирование результата
        print(f"🔹 {last_name} {first_name} {sur_name}: {result}")

        # Сохранение результата
        test_results.append([last_name, first_name, sur_name, result])

# === Запись результатов в CSV ===
with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Фамилия", "Имя", "Отчество", "Результат"])
    writer.writerows(test_results)

print("\n📜 Тестирование завершено! Результаты сохранены в", RESULTS_FILE)
