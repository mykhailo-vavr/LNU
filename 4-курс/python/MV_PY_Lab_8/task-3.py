import urllib.request
from os import startfile

url = "https://www.w3schools.com/xml/plant_catalog.xml"

try:
    print(f"Починаємо виконувати GET-запит до вказаної URL-адреси ({url})...")

    # Виконуємо GET-запит та отримуємо вміст відповіді
    with urllib.request.urlopen(url) as response:
        content = response.read()
        print(f"Успішно отримали дані за URL-адресою {url}")

    # Зберігаємо отримані дані у файл task-3-data.xml
    with open("task-3-data.xml", "wb") as file:
        file.write(content)

    # Виводимо повідомлення про успішне завершення операцій
    print(f"Збережено у файл task-3-data.xml. Запускаємо файл на виконання.")

    # Запускаємо файл task-3-data.xml за допомогою стандартної функції startfile
    startfile("task-3-data.xml")

except urllib.error.URLError as e:
    # Обробка помилок, які можуть виникнути при виконанні запиту
    print(f"Виникла помилка запиту: {e.reason}")

except Exception as e:
    # Обробка інших невідомих помилок
    print(f"Виникла невідома помилка: {e}")
