import os, subprocess
import json
from pprint import pprint

filename = "data.json"

print("Безпосередньо переглядаємо сам файл, запустивши на виконання дочірній процес")
current_dir_path = os.path.abspath(".")
subprocess.Popen(["code", os.path.join(current_dir_path, filename)])

print("Перетворюємо json-файл у внутрішнє зображення і друкуємо у вікні виконання")
with open(filename) as file:
    data = json.load(file)
pprint([data[0], data[1], data[3], data[3], data[4], data[5]])
