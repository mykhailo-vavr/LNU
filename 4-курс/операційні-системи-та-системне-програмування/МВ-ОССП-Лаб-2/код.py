import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
from datetime import datetime

class FileOperationsApp:
    def __init__(self, master):
        self.master = master
        master.title("Операції з файлами")

        # Ініціалізація логування
        self.init_logging()
        self.log("Запуск програми")

        # Створення кнопок та інших елементів інтерфейсу
        self.create_buttons()
        self.create_treeview()
        self.create_text_area()

    def init_logging(self):
        # Відкриття файлу для логування
        self.log_file = open("logs.txt", "a")

    def log(self, message):
        # Запис повідомлення у файл логування
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_file.write(f"{timestamp} = {message}\n")
        self.log_file.flush()  # Забезпечення негайного запису

    def create_buttons(self):
        # Створення кнопок з відповідними функціями
        self.log("Створення кнопок з відповідними функціями")
        buttons_info = [
            ("Показати імена файлів", self.show_file_names),
            ("Показати повний шлях від кореня логічного диску до файлів", self.show_full_paths),
            ("Показати властивості файлів", self.show_file_properties),
            ("Порахувати суму чисел файлу", self.show_sum_calculation_modal)
        ]

        for text, command in buttons_info:
            button = tk.Button(self.master, text=text, command=command)
            button.pack(pady=10)

    def create_treeview(self):
        # Створення дерева Treeview для відображення файлів
        self.log("Створення дерева Treeview для відображення файлів")
        self.files_tree = ttk.Treeview(self.master, columns=("File Path",))
        self.files_tree.heading("#0", text="Шлях до файлу")
        self.files_tree.pack(side=tk.LEFT, fill=tk.Y)

        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.files_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_tree.configure(yscrollcommand=scrollbar.set)

        # Заповнення дерева Treeview файлами .dat
        self.populate_treeview()
        self.files_tree.bind("<Double-1>", self.on_file_select)

    def create_text_area(self):
        # Створення текстової області для відображення вмісту файлів
        self.log("Створення текстової області для відображення вмісту файлів")
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def populate_treeview(self):
        # Знаходження файлів .dat та їх відображення в дереві Treeview
        self.log("Знаходження файлів .dat та їх відображення в дереві Treeview")
        dat_files = self.find_dat_files()
        for file in dat_files:
            self.files_tree.insert("", tk.END, values=(file,))

    def find_dat_files(self):
        # Пошук файлів з розширенням .dat у поточному каталозі та підкаталогах
        self.log("Пошук файлів з розширенням .dat у поточному каталозі та підкаталогах")
        return [os.path.join(root, file) for root, _, files in os.walk(".") for file in files if file.endswith(".dat")]

    def show_file_content(self, file_path):
        # Відображення вмісту обраного файлу у текстовій області
        self.log("Відображення вмісту обраного файлу у текстовій області")
        try:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
        except FileNotFoundError:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Файл не знайдено")

    def on_file_select(self, event):
        # Обробка подвійного кліку на файл у дереві Treeview
        selection = event.widget.selection()
        if selection:
            selected_file = event.widget.item(selection[0])['values'][0]
            self.show_file_content(selected_file)

    def show_sum_calculation_modal(self):
        # Відображення модального вікна для розрахунку суми
        self.log("Відкриття модального вікна для розрахунку суми")

        modal = tk.Toplevel(self.master)
        modal.title("Обчислення суми")
        modal.geometry("300x150")

        replacement_label = tk.Label(modal, text="Число яким заміняти:")
        replacement_label.pack(pady=(10, 0))

        replacement_entry = tk.Entry(modal)
        replacement_entry.pack(pady=5)

        calculate_button = tk.Button(modal, text="Порахувати", command=lambda: self.calculate_sum(replacement_entry.get(), modal))
        calculate_button.pack(pady=10)

    def calculate_sum(self, replacement_number, modal):
        # Розрахунок суми чисел у файлах з можливістю заміни некоректних значень
        self.log("Розрахунок суми чисел у файлах з можливістю заміни некоректних значень")
        try:
            replacement_number = float(replacement_number)
        except ValueError:
            messagebox.showerror("Помилка", "Невалідне число для заміни.")
            return

        files = self.find_dat_files()
        if files:
            for file in files:
                total_sum = 0
                replacements = []
                try:
                    with open(file, "r+") as f:
                        lines = f.readlines()
                        corrected_lines = []
                        for line in lines:
                            try:
                                number = float(line.strip())
                            except ValueError:
                                replacements.append((line.strip(), replacement_number))
                                corrected_lines.append(f"{replacement_number}\n")
                                continue
                            corrected_lines.append(line)
                            total_sum += number
                        f.seek(0)
                        f.truncate()
                        f.writelines(corrected_lines)
                    messagebox.showinfo("Обчислення суми", f"Суми чисел у файлі {file}: {total_sum}\nЗаміни: {replacements}")
                except FileNotFoundError:
                    messagebox.showerror("Помилка", f"Файл {file} не знайдено")
        else:
            messagebox.showinfo("Обчислення суми", "Не знайдено .dat файлів")

        modal.destroy()

    def show_file_names(self):
        # Відображення імен файлів у вікні
        self.log("Відображення імен файлів у вікні")
        files = self.find_dat_files()
        if files:
            content = "\n".join([file.split("/")[-1] for file in files ])
        else:
            content = "Не знайдено .dat файлів"
        self.show_file_info_window("Імена файлів", content)

    def show_full_paths(self):
        # Відображення повних шляхів файлів у вікні
        self.log("Відображення повних шляхів файлів у вікні")
        files = self.find_dat_files()
        if files:
            content = "\n".join([os.path.abspath(file) for file in files])
        else:
            content = "Не знайдено .dat файлів"
        self.show_file_info_window("Повні шляхи", content)

    def show_file_properties(self):
        # Відображення властивостей файлів у вікні
        self.log("Відображення властивостей файлів у вікні")
        files = self.find_dat_files()
        if files:
            result_window = tk.Toplevel(self.master)
            result_window.title("Властивості файлів")
            result_window.geometry("800x600")
            
            properties_tree = ttk.Treeview(result_window, columns=("File Path", "Size (KB)", "Modified Time", "Created Time", "Accessed Time", "Owner", "Mode", "Inode", "Device"))
            properties_tree.heading("File Path", text="Шлях до файлу")
            properties_tree.heading("Size (KB)", text="Розмір (KB)")
            properties_tree.heading("Modified Time", text="Змінено")
            properties_tree.heading("Created Time", text="Створено")
            properties_tree.heading("Accessed Time", text="Відкрито")
            properties_tree.heading("Owner", text="Власник")
            properties_tree.heading("Mode", text="Режим")
            properties_tree.heading("Inode", text="Індексний дескриптор")
            properties_tree.heading("Device", text="Пристрій")
            properties_tree.pack(expand=True, fill=tk.BOTH)

            for file in files:
                file_name = os.path.basename(file)
                file_stat = os.stat(file)
                file_size = file_stat.st_size / 1024  # Convert bytes to KB
                file_modified_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                file_created_time = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                file_accessed_time = datetime.fromtimestamp(file_stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
                file_owner = file_stat.st_uid
                file_mode = file_stat.st_mode
                file_inode = file_stat.st_ino
                file_device = file_stat.st_dev
                
                properties_tree.insert("", tk.END, values=(file, file_name, f"{file_size:.2f}", file_modified_time, file_created_time, file_accessed_time, file_owner, file_mode, file_inode, file_device))
        else:
            result_window = tk.Toplevel(self.master)
            result_window.title("Властивості файлів")
            result_window.geometry("200x100")
            
            no_files_label = tk.Label(result_window, text="Не знайдено .dat файлів")
            no_files_label.pack(pady=10)

    def show_file_info_window(self, title, content):
        # Відображення вікна з інформацією про файли
        self.log("Відображення вікна з інформацією про файли")
        result_window = tk.Toplevel(self.master)
        result_window.title(title)
        result_window.geometry("800x600")
        
        label = tk.Label(result_window, text=content)
        label.pack(expand=True, fill=tk.BOTH)

    def __del__(self):
        # Закриття файлу логування при завершенні роботи програми
        self.log("Закриття файлу логування при завершенні роботи програми")
        self.log("Завершення роботи програми")
        self.log_file.close()

root = tk.Tk()
app = FileOperationsApp(root)
root.mainloop()
