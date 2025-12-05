import requests
import json
import random

url = "http://155.212.169.230:8000/webhook"

# Генерация случайных данных для теста
random_id = random.randint(100, 999)

payload = {
    "nickname": f"Player_{random_id}",
    "server": "Polit 1",
    "realname": f"TestUser_{random_id}",
    "age": str(random.randint(14, 30)),
    "contact": f"@test_user_{random_id}"
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
