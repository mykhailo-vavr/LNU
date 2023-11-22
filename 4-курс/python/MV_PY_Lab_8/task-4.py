import xml.etree.ElementTree as ET

# Опрацювання XML-файлу з інформацією про рослини


def read_xml_file(file_path):
    """
    Функція для зчитування XML-файлу та повернення кореневого елементу.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


def get_plant_info(plant_element):
    """
    Функція для отримання інформації про рослину з елементу.
    """
    common_name = plant_element.find("COMMON").text
    botanical_name = plant_element.find("BOTANICAL").text
    zone = plant_element.find("ZONE").text
    light = plant_element.find("LIGHT").text
    price = plant_element.find("PRICE").text
    availability = plant_element.find("AVAILABILITY").text

    return {
        "Common Name": common_name,
        "Botanical Name": botanical_name,
        "Zone": zone,
        "Light": light,
        "Price": price,
        "Availability": availability,
    }


def find_plants_by_light(root, light_type):
    """
    Функція для знаходження рослин за типом освітлення.
    """
    matching_plants = []
    for plant_element in root.findall("PLANT"):
        light = plant_element.find("LIGHT").text
        if light.lower() == light_type.lower():
            plant_info = get_plant_info(plant_element)
            matching_plants.append(plant_info)
    return matching_plants


def find_plants_by_zone(root, zone):
    """
    Функція для знаходження рослин за зонами вирощування.
    """
    matching_plants = []
    for plant_element in root.findall("PLANT"):
        plant_zone = plant_element.find("ZONE").text
        if plant_zone == zone:
            plant_info = get_plant_info(plant_element)
            matching_plants.append(plant_info)
    return matching_plants


def get_average_price(root):
    """
    Функція для знаходження середньої ціни на рослини.
    """
    prices = [
        float(plant_element.find("PRICE").text[1:])
        for plant_element in root.findall("PLANT")
    ]
    average_price = sum(prices) / len(prices)
    return round(average_price, 2)


def main():
    # Зчитуємо XML-файл
    xml_file_path = "task-3-data.xml"
    root = read_xml_file(xml_file_path)

    # Задача 1: Вивести кількість рослин у каталозі
    plant_count = len(root.findall("PLANT"))
    print(f"Кількість рослин у каталозі: {plant_count}\n")

    # Задача 2: Вивести інформацію про кожну рослину
    for plant_element in root.findall("PLANT"):
        plant_info = get_plant_info(plant_element)
        print("Рослина:")
        for prop, value in plant_info.items():
            print(f"\t{prop}: {value}")
        print("\n")

    # Задача 3: Знайти рослини, які ростуть в зоні 4
    plants_in_zone_4 = find_plants_by_zone(root, "4")
    print("Рослини, які ростуть в зоні 4:")
    for plant in plants_in_zone_4:
        print(plant)
    print("\n")

    # Задача 4: Знайти рослини, які ростуть на сонці
    sunny_plants = find_plants_by_light(root, "Sun")
    print("Рослини, які ростуть на сонці:")
    for plant in sunny_plants:
        print(plant)
    print("\n")

    # Задача 5: Знайти середню ціну на рослини
    average_price = get_average_price(root)
    print(f"Середня ціна на рослини: ${average_price}")


if __name__ == "__main__":
    main()
