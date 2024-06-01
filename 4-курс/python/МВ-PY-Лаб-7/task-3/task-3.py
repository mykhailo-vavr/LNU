import subprocess
from os import path


def main():
    current_dir_path = path.abspath(".")
    print(f"== Основний процес == Поточна директорія: {current_dir_path}")

    text_file_path = path.join(current_dir_path, "file.txt")
    print(f"== Основний процес == Отримано шлях до .txt файлу: {text_file_path}")

    print("== Основний процес == Зчитуємо початковий вміст файлу:")
    with open(text_file_path, "r", encoding="utf8") as file:
        content = file.read()
    print("== Основний процес == Початковий вміст файлу")
    print(content)

    exe_file_path = path.join(current_dir_path, "child-process.exe")
    print(f"== Основний процес == Отримано шлях до .exe файлу: {exe_file_path}")

    print("== Основний процес == Запускаємо дочірній процес")
    subprocess.run(["child-process"], cwd=current_dir_path)

    print("== Основний процес == Зчитуємо оновлений вміст файлу")
    with open(text_file_path, "r", encoding="utf8") as file:
        modified_content = file.read()
    print("== Основний процес == Оновлений вміст файлу:")
    print(modified_content)


if __name__ == "__main__":
    main()
