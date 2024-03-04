import json


with open("data.json") as json_file:
    data = json.load(json_file)

with open("task3-результат.txt", "w", encoding="utf8") as file:
    document_type_message = f"Тип цілого документа: {type(data).__name__}\n"
    file.writelines(document_type_message)
    print(document_type_message)

    list_length_message = f"Список має {len(data)} елементів\n"
    file.writelines(list_length_message)
    print(list_length_message)

    isEqual = True
    prevItem = data[0]
    for item in data:
        isEqual = item.keys() == prevItem.keys() and [
            type(value).__name__ for value in item.values()
        ] == [type(value).__name__ for value in prevItem.values()]
        prevItem = item

    schema_match_message = (
        f"Чи всі елементи списку мають однакову схему даних: {isEqual}\n"
    )
    file.write(schema_match_message)
    print(schema_match_message)

    type_of_elements_message = f"Тип елементів списку: {type(data[0]).__name__}\n"
    file.write(type_of_elements_message)
    print(type_of_elements_message)

    keys_and_types_message = f"Ключі та тип елементів списку: {[[key, type(value).__name__] for key, value in data[0].items()]}\n"
    file.write(keys_and_types_message)
    print(keys_and_types_message)
