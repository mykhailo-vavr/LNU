import urllib.request
from os import startfile

# Задача 1
url = "https://hnrss.org/newest"

# Задача 2
try:
    print(f"Починаємо виконувати GET-запит до вказаної URL-адреси ({url})...")

    # Виконуємо GET-запит та отримуємо вміст відповіді
    with urllib.request.urlopen(url) as response:
        content = response.read()
        print(f"Успішно отримали дані за URL-адресою {url}")

    # Зберігаємо отримані дані у файл task-1-2-data.xml
    with open("task-1-2-data.xml", "wb") as file:
        file.write(content)

    # Виводимо повідомлення про успішне завершення операцій
    print(f"Збережено у файл task-1-2-data.xml. Запускаємо файл на виконання.")

    # Запускаємо файл task-1-2-data.xml за допомогою стандартної функції startfile
    startfile("task-1-2-data.xml")

except urllib.error.URLError as e:
    # Обробка помилок, які можуть виникнути при виконанні запиту
    print(f"Виникла помилка запиту: {e.reason}")

except Exception as e:
    # Обробка інших невідомих помилок
    print(f"Виникла невідома помилка: {e}")
