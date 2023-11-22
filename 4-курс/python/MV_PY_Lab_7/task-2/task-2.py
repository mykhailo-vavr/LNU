from os import path, execv
from glob import glob


def task2():
    current_dir_path = path.abspath(".")
    print(f"Поточна директорія: {current_dir_path}")

    files_paths_list = glob(path.join(current_dir_path, "*.txt"))
    print(f"Отримано список шляхів до файлів: {files_paths_list}")

    vscode_exe_path = path.join(
        "C:/Users",
        "ElitexAdmin",
        "AppData",
        "Local",
        "Programs",
        "Microsoft VS Code",
        "Code.exe",
    )
    print(f"Створено шлях до виконуваного файлу VS Code: {vscode_exe_path}")

    print(f"Запускаємо виконуваний файл VS Code")
    execv(vscode_exe_path, [" "] + files_paths_list)


if __name__ == "__main__":
    task2()
