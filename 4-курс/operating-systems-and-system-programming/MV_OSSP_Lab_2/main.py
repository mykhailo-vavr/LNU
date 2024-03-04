import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def read_data(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                num = float(line.strip())
                data.append(num)
            except ValueError:
                data.append(0)  # Виправляємо неправильні записи даних числом 0
    return data


def show_full_file_paths():
    file_paths = glob.glob("**/*.dat", recursive=True)
    for file_path in file_paths:
        print(f"Повне ім'я файлу: {os.path.abspath(file_path)}")


def show_full_path_from_root():
    file_paths = glob.glob("**/*.dat", recursive=True)
    for file_path in file_paths:
        root_path = os.path.abspath(os.sep)
        full_path = os.path.relpath(file_path, start=root_path)
        print(f"Повний шлях від кореня логічного диску: {full_path}")


def show_file_info():
    file_paths = glob.glob("**/*.dat", recursive=True)
    headers = ["Повне ім'я", "Розмір (байт)", "Дата створення", "Дата редагування"]
    data = []
    for file_path in file_paths:
        file_stat = os.stat(file_path)
        full_name = os.path.abspath(file_path)
        size = file_stat.st_size
        created_time = file_stat.st_ctime
        modified_time = file_stat.st_mtime
        data.append((full_name, size, created_time, modified_time))

    table_window = tk.Toplevel(root)
    table_window.title("Інформація про файли")

    tree = ttk.Treeview(table_window, columns=headers, show="headings")
    for header in headers:
        tree.heading(header, text=header)

    for item in data:
        tree.insert("", "end", values=item)

    tree.pack(expand=True, fill="both")


def show_file_content():
    file_path = filedialog.askopenfilename(filetypes=[("DAT files", "*.dat")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            content_window = tk.Toplevel(root)
            content_window.title("Вміст файлу")
            text = tk.Text(content_window)
            text.insert(tk.END, content)
            text.pack()


def fix_data_and_sum():
    file_path = filedialog.askopenfilename(filetypes=[("DAT files", "*.dat")])
    if file_path:
        data = read_data(file_path)
        # Виправлення неправильних записів
        fixed_value = float(
            input("Введіть число, яким бажаєте замінити неправильні записи: ")
        )
        fixed_data = [fixed_value if x == 0 else x for x in data]
        # Обчислення суми
        total_sum = sum(fixed_data)
        print(f"Сума чисел у файлі після виправлення: {total_sum}")


root = tk.Tk()
root.title("File Operations")

button1 = tk.Button(
    root, text="Показати повні імена файлів", command=show_full_file_paths
)
button1.pack(pady=5)

button2 = tk.Button(
    root,
    text="Показати повний шлях від кореня логічного диску",
    command=show_full_path_from_root,
)
button2.pack(pady=5)

button3 = tk.Button(root, text="Показати інформацію про файли", command=show_file_info)
button3.pack(pady=5)

button4 = tk.Button(root, text="Показати вміст файлу", command=show_file_content)
button4.pack(pady=5)

button5 = tk.Button(
    root, text="Виправити дані та порахувати суму", command=fix_data_and_sum
)
button5.pack(pady=5)

root.mainloop()
