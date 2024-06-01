import urllib.request

try:
    url = "https://jsonplaceholder.typicode.com/photos"
    print(f"Починаємо виконувати GET-запит до вказаної URL-адреси ({url})...")

    with urllib.request.urlopen(url) as response:
        content = response.read()
        print(f"Успішно отримали дані за URL-адресою {url}")

    with open("data.json", "wb") as file:
        file.write(content)
    print(f"Збережено у файл data.json")


except urllib.error.URLError as e:
    print(f"Виникла помилка запиту: {e.reason}")

except Exception as e:
    print(f"Виникла невідома помилка: {e}")
