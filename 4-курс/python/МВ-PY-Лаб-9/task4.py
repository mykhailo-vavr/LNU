import json

with open("data.json") as json_file:
    data = json.load(json_file)

"""
Задача 1
Знайти та надрукувати кількість альбомів
"""
unique_albums = set(photo["albumId"] for photo in data)
number_of_albums = len(unique_albums)

print(f"Кількість альбомів: {number_of_albums}")


"""
Задача 2
Знайти та надрукувати найпопулярніший альбом та кількість зображень у ньому
"""
album_counts = {}

for item in data:
    album_id = item.get("albumId", "")

    album_counts[album_id] = album_counts.get(album_id, 0) + 1

most_popular_album = max(album_counts, key=album_counts.get)
count_of_images = album_counts[most_popular_album]

print(
    f"Найпопулярніший альбом: {most_popular_album}, Кількість зображень: {count_of_images}"
)
