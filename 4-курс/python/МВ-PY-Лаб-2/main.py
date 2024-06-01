import json
import csv
from enum import Enum
from datetime import datetime


class WeatherDataKeysEnum(str, Enum):
    """
    Перерахування для ключів метеоданих. Використовується для однозначного визначення полів у метеоданих.
    """

    ID = "id"
    CITY = "city"
    DATE = "date"
    TEMPERATURE = "temperature"
    DESCRIPTION = "description"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    WIND_DIRECTION = "wind_direction"
    CLOUD_TYPE = "cloud_type"
    PRESSURE = "pressure"
    UV_LEVEL = "uv_level"
    AIR_QUALITY_INDEX = "air_quality_index"
    SUNRISE = "sunrise"
    SUNSET = "sunset"


class CloudTypeEnum(str, Enum):
    """
    Перерахування для типів хмарності. Визначає константи для різних типів хмар.
    """

    CLEAR = "clear"
    CLOUDY = "cloudy"


class WindDirectionEnum(str, Enum):
    """
    Перерахування для напрямків вітру. Визначає константи для різних напрямків вітру.
    """

    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class SortOrderEnum(str, Enum):
    """
    Перерахування для порядку сортування. Визначає константи для зростання (ASC) та спадання (DESC) порядку.
    """

    ASC = "asc"
    DESC = "desc"


class WeatherCollection:
    def __init__(self, data: list[dict] = []):
        """
        Ініціалізує екземпляр класу WeatherCollection з заданими даними.

        Аргументи:
            data (list[dict]): Список словників, що містить метеодані.
        """
        self.__data = data

    def get_data(self):
        """
        Повертає метеодані, що зберігаються в колекції.

        Повертає:
            list[dict]: Метеодані.
        """
        return self.__data

    def set_data(self, data: list[dict]):
        """
        Встановлює метеодані в колекції.

        Аргументи:
            data (list[dict]): Нові метеодані, які потрібно встановити.
        """
        self.__data = data

    def get_all(self, **query):
        """
        Отримує відфільтровані та відсортовані метеодані на основі наданих параметрів запиту.

        Аргументи:
            **query: Ключові аргументи для фільтрації та сортування даних.
                - search (str): Використовується для пошуку за назвою міста або описом погоди.
                - wind_direction (WindDirectionEnum): Фільтрує дані за напрямком вітру (за значенням з WindDirectionEnum).
                - cloud_type (CloudTypeEnum): Фільтрує дані за типом хмар (за значенням з CloudTypeEnum).
                - sort (WeatherDataKeysEnum): Поле для сортування метеоданих (за значенням з WeatherDataKeysEnum).
                              За замовчуванням використовується WeatherDataKeysEnum.ID.
                - order (SortOrderEnum): Порядок сортування. Може бути SortOrderEnum.ASC (за зростанням) або
                               SortOrderEnum.DESC (за спаданням). За замовчуванням ASC.

        Повертає:
            list[dict]: Відфільтровані та відсортовані метеодані.
        """
        search = query.get("search", "")
        wind_direction = query.get("wind_direction", "")
        cloud_type = query.get("cloud_type", "")
        sort = query.get("sort", WeatherDataKeysEnum.ID)
        order = query.get("order", SortOrderEnum.ASC)

        filtered_result = []

        for item in self.__data:
            if (
                (
                    search == ""
                    or (
                        search in item[WeatherDataKeysEnum.CITY]
                        or search in item[WeatherDataKeysEnum.DESCRIPTION]
                    )
                )
                and (
                    wind_direction not in WindDirectionEnum
                    or wind_direction == item[WeatherDataKeysEnum.WIND_DIRECTION]
                )
                and (
                    cloud_type not in CloudTypeEnum
                    or cloud_type == item[WeatherDataKeysEnum.CLOUD_TYPE]
                )
            ):
                filtered_result.append(item)

        sorted_and_filtered_result = sorted(
            filtered_result,
            key=lambda x: x[sort],
            reverse=False if order == SortOrderEnum.ASC else True,
        )

        return sorted_and_filtered_result

    def get_by_pk(self, id: int):
        """
        Отримує метеодані за первинним ключем.

        Аргументи:
            id (int): Первинний ключ для пошуку.

        Повертає:
            dict або None: Метеодані, якщо знайдено, в іншому випадку None.
        """
        for item in self.__data:
            if item["id"] == id:
                return item

        return None

    def get_lowest_temperature(self):
        """
        Отримує запис з найнижчою температурою серед метеоданих.

        Повертає:
            dict: Метеодані з найнижчою температурою.
        """
        result = min(self.__data, key=lambda x: x[WeatherDataKeysEnum.TEMPERATURE])
        return result

    def get_highest_temperature(self):
        """
        Отримує запис з найвищою температурою серед метеоданих.

        Повертає:
            dict: Метеодані з найвищою температурою.
        """
        result = max(self.__data, key=lambda x: x[WeatherDataKeysEnum.TEMPERATURE])
        return result

    def get_average_temperature(self):
        """
        Обчислює та повертає середню температуру серед метеоданих.

        Повертає:
            float: Середня температура.
        """
        if len(self.__data) == 0:
            return 0

        temperature_sum = 0
        for item in self.__data:
            temperature_sum += item[WeatherDataKeysEnum.TEMPERATURE]

        return temperature_sum / len(self.__data)

    def get_longest_day(self):
        """
        Отримує запис, що представляє найдовший день за часами сходу та заходу сонця.

        Повертає:
            dict: Метеодані, що представляють найдовший день.
        """
        result = max(
            self.__data,
            key=lambda x: datetime.strptime(x["sunset"], "%I:%M %p")
            - datetime.strptime(x["sunrise"], "%I:%M %p"),
        )
        return result


class WeatherReader:
    def __init__(self, weather_collection: WeatherCollection):
        """
        Ініціалізує екземпляр класу WeatherReader.

        Аргументи:
            weather_collection (WeatherCollection): Колекція для зберігання метеоданих.
        """
        self.__weather_collection = weather_collection

    def from_json_file(self, file_path: str):
        """
        Зчитує метеодані з файлу у форматі JSON та завантажує їх у WeatherCollection.

        Аргументи:
            file_path (str): Шлях до файлу JSON з метеоданими.
        """
        try:
            with open(file_path, "r", encoding="utf8") as file:
                data = json.load(file)
                self.__weather_collection.set_data(data)
        except FileNotFoundError:
            print(f"Файл {file_path} не знайдено")
        except:
            print("Помилка читання json файлу")


def write_to_json(file_path: str, data):
    """
    Записує дані у JSON файл.

    Аргументи:
        file_path (str): Шлях до файлу JSON для запису даних.
        data: Дані для запису у файл.
    """
    try:
        with open(file_path, "w", encoding="utf8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )
    except:
        print("Помилка запису у json файл")


def write_to_csv(file_path: str, data, fieldnames: list[str]):
    """
    Записує дані у CSV файл.

    Аргументи:
        file_path (str): Шлях до файлу CSV для запису даних.
        data: Дані для запису у файл.
        fieldnames (list[str]): Список назв стовпців у CSV файлі.
    """
    try:
        with open(file_path, "w", encoding="utf8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except:
        print("Помилка запису у csv файл")


def ask_user_save_results(data):
    """
    Питає користувача, чи бажає він зберегти результат у файл, і викликає відповідну функцію запису.

    Аргументи:
        data: Результат, який може бути записаний.
    """
    print_option = input("Бажаєте вивести результат у консоль? (y/n): ").lower()
    if print_option == "y":
        print(data)

    save_option = input("Бажаєте зберегти результат у файл? (y/n): ").lower()

    if save_option == "y":
        file_path = input("Введіть шлях до файлу для збереження результату: ")
        save_format = input("Виберіть формат файлу (json/csv): ").lower()

        if save_format == "json":
            write_to_json(file_path, data)
        elif save_format == "csv":
            fieldnames = list(data[0].keys()) if data else []
            write_to_csv(file_path, data, fieldnames)
        else:
            print("Невірний формат файлу. Результат не буде збережено.")


def Testorg():
    weather_collection = WeatherCollection()

    weather_reader = WeatherReader(weather_collection)
    weather_reader.from_json_file("./InData.json")

    while True:
        print("\nКоманди:")
        print("1. Вивести всі дані")
        print("2. Знайти за ID")
        print("3. Найнижча температура")
        print("4. Найвища температура")
        print("5. Середня температура")
        print("6. Найдовший день")
        print("0. Вихід")

        choice = input("Введіть номер команди: ")

        if choice == "1":
            search = input("Введіть текст для пошуку у назвах міст або опису погоди: ")
            wind_direction = input(
                "Введіть напрям вітру north/east/south/west (або залиште порожнім для ігнорування): "
            )
            cloud_type = input(
                "Введіть тип хмар cloudy/clear (або залиште порожнім для ігнорування): "
            )
            sort = (
                input(
                    "Введіть поле для сортування id/city/temperature/description/humidity/pressure (або залиште порожнім для сортування за ID): "
                )
                or WeatherDataKeysEnum.ID
            )
            order = input("Введіть порядок сортування asc/desc): ") or SortOrderEnum.ASC

            query = {
                "search": search,
                "wind_direction": wind_direction,
                "cloud_type": cloud_type,
                "sort": sort,
                "order": order,
            }
            result = weather_collection.get_all(**query)

            ask_user_save_results(result)

        elif choice == "2":
            id_to_find = int(input("Введіть ID для пошуку: "))
            result = weather_collection.get_by_pk(id_to_find)

            ask_user_save_results([result])

        elif choice == "3":
            result = weather_collection.get_lowest_temperature()

            ask_user_save_results([result])

        elif choice == "4":
            result = weather_collection.get_highest_temperature()

            ask_user_save_results([result])

        elif choice == "5":
            result = weather_collection.get_average_temperature()

            ask_user_save_results([result])

        elif choice == "6":
            result = weather_collection.get_longest_day()

            ask_user_save_results([result])

        elif choice == "0":
            print("Дякую за використання. До побачення!")
            break
        else:
            print("Невірна команда. Будь ласка, введіть коректний номер команди.")


if __name__ == "__main__":
    Testorg()
