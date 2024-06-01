import os
import json


def FnSol1(arr):
    count_positive = 0
    count_negative = 0
    sum_negative = 0

    try:
        for number in arr:
            if number == 0:
                break
            elif number > 0:
                count_positive += 1
            else:
                count_negative += 1
                sum_negative += number

        average_negative = sum_negative / count_negative if count_negative > 0 else 0

        return count_positive, count_negative, average_negative
    except TypeError:
        return "Помилка типу даних"
    except ValueError:
        return "Помилка формату даних"
    except:
        return "Невідома помилка"


def FnSol2(dict):
    try:
        a = dict["a"]
        b = dict["b"]
        c = dict["c"]

        if a <= 0 or b <= 0 or c <= 0:
            return "Довжини відрізків повинні бути додатними числами"

        if a + b > c and a + c > b and b + c > a:
            if a == b == c:
                return "Рівносторонній трикутник"
            elif a == b or a == c or b == c:
                return "Рівнобедрений трикутник"
            else:
                return "Різносторонній трикутник"
        else:
            return "Неможливо утворити трикутник"
    except TypeError:
        return "Помилка типу даних"
    except ValueError:
        return "Помилка формату даних"
    except:
        return "Невідома помилка"


def FnSol3(data):
    try:
        if not isinstance(data, str):
            raise TypeError()

        words = data.strip().split()
        result = os.linesep.join(words)
        return result
    except TypeError:
        return "Помилка типу даних"
    except ValueError:
        return "Помилка формату даних"
    except:
        return "Невідома помилка"


def FnSol4(matrix):
    try:
        if len(matrix) == 0:
            raise ValueError()

        for row in matrix:
            if len(row) != len(matrix):
                raise ValueError()

        rows = cols = len(matrix)
        max_sum = float("-inf")
        top, bottom, left, right = 0, 0, 0, 0

        for i in range(rows):
            for j in range(cols):
                for k in range(i, rows):
                    for l in range(j, cols):
                        current_sum = sum(
                            matrix[x][y]
                            for x in range(i, k + 1)
                            for y in range(j, l + 1)
                        )
                        if current_sum > max_sum:
                            max_sum = current_sum
                            top, bottom, left, right = i, k, j, l

        return max_sum, (top, left), (bottom, right)
    except TypeError as e:
        print(e)
        return "Помилка типу даних"
    except ValueError as e:
        print(e)
        return "Помилка формату даних"
    except:
        return "Невідома помилка"


def Testorg():
    def read_json_file(file_path):
        try:
            with open(file_path, "r", encoding="utf8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Файл {file_path} не знайдено")
            return None
        except json.JSONDecodeError as e:
            print(f"Помилка декодування JSON: {e}")
            return None
        except:
            print("Невідома помилка")

    def write_json_file(file_path, data):
        try:
            with open(file_path, "w", encoding="utf8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except:
            print("Невідома помилка")

    def perform_test_cycle(input_file_path, output_file_path, func):
        data = read_json_file(input_file_path)
        results_arr = []

        for item in data:
            output_data = func(item["data"])
            results_arr.append(
                {
                    "test_type": item["test_type"],
                    "comment": item["comment"],
                    "input_data": item["data"],
                    "output_data": output_data,
                }
            )

        write_json_file(output_file_path, results_arr)

    while True:
        print("\nКоманди:")
        print("1. FnSol1")
        print("2. FnSol2")
        print("3. FnSol3")
        print("4. FnSol4")
        print("0. Вихід")

        option = input()

        if option == "0":
            break

        if option == "1":
            perform_test_cycle("./InData1.json", "./Res1.json", FnSol1)
        elif option == "2":
            perform_test_cycle("./InData2.json", "./Res2.json", FnSol2)
        elif option == "3":
            perform_test_cycle("./InData3.json", "./Res3.json", FnSol3)
        elif option == "4":
            perform_test_cycle("./InData4.json", "./Res4.json", FnSol4)
        else:
            print("Ви ввели неправильний номер Команди")


if __name__ == "__main__":
    Testorg()
