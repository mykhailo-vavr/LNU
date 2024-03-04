import tkinter as tk
from tkinter import filedialog


def read_file(file_path, encoding):
    try:
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return "Error: " + str(e)


def edit_file(file_path, new_content, encoding):
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(new_content)
        return "File edited successfully."
    except Exception as e:
        return "Error: " + str(e)


def open_file():
    file_path = filedialog.askopenfilename()

    if file_path:
        encoding = encoding_var.get()
        content = read_file(file_path, encoding)
        text.delete("1.0", tk.END)
        text.insert(tk.END, content)


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")

    if file_path:
        encoding = encoding_var.get()
        content = text.get("1.0", tk.END)
        result = edit_file(file_path, content, encoding)
        status_bar.config(text=result)


# Create the main window
root = tk.Tk()
root.title("Text File Editor")

# Create a text widget
text = tk.Text(root, wrap="word")
text.pack(expand=True, fill="both")

# Encoding selection dropdown menu
encoding_var = tk.StringVar(root)
encoding_var.set("utf-8")  # Default encoding is UTF-8
encoding_menu = tk.OptionMenu(root, encoding_var, "utf-8", "windows-1251")
encoding_menu.pack()

# Create buttons for open and save
open_button = tk.Button(root, text="Open", command=open_file)
open_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = tk.Button(root, text="Save", command=save_file)
save_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a status bar
status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
