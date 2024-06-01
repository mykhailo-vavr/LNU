from os import path, startfile
from glob import glob


def task1():
    current_dir_path = path.abspath(".")
    print(f"Поточна директорія: {current_dir_path}")

    docx_file_path = glob(path.join(current_dir_path, "*.docx"))[0]
    print(f"Отримано шлях до .docx файлу: {docx_file_path}")

    startfile(docx_file_path)
    print(f"Запускаємо .docx файл")

    jpeg_file_path = glob(path.join(current_dir_path, "*.jpeg"))[0]
    print(f"Отримано шлях до .jpeg файлу: {jpeg_file_path}")

    startfile(jpeg_file_path)
    print(f"Запускаємо .jpeg файл")


if __name__ == "__main__":
    task1()
