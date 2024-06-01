import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt


def phasespace(n):
    """
    Функція для побудови фазового портрету.

    Параметри:
    n (numpy array): Досліджувана часова послідовність.
    """
    embedding_dimension = 3  # Розмір вбудовування (фазового простору)
    time_delay = 1  # Затримка у часі

    # Створення вбудованої матриці
    embedded_matrix = []
    for i in range(len(n) - (embedding_dimension - 1) * time_delay):
        embedded_matrix.append(
            [n[i + j * time_delay] for j in range(embedding_dimension)]
        )
    embedded_matrix = np.array(embedded_matrix)

    # Візуалізація фазового портрету
    if embedding_dimension == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(embedded_matrix[:, 0], embedded_matrix[:, 1], embedded_matrix[:, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Фазовий портрет")
        plt.show()
    else:
        plt.plot(embedded_matrix[:, 0], embedded_matrix[:, 1])
        plt.xlabel("Фазова координата 1")
        plt.ylabel("Фазова координата 2")
        plt.title("Фазовий портрет")
        plt.show()


def crp(a, embedding_dimension=3, time_delay=1):
    """
    Функція для побудови рекурентної карти.

    Параметри:
    a (list або numpy array): Вихідний часовий ряд.
    embedding_dimension (int): Розмір вбудовування (за замовчуванням 3).
    time_delay (int): Затримка у часі (за замовчуванням 1).
    """
    # Створення вбудованої матриці
    embedded_matrix = []
    for i in range(len(a) - (embedding_dimension - 1) * time_delay):
        embedded_matrix.append(
            [a[i + j * time_delay] for j in range(embedding_dimension)]
        )
    embedded_matrix = np.array(embedded_matrix)

    # Обчислення відстаней між точками
    distances = np.zeros((len(embedded_matrix), len(embedded_matrix)))
    for i in range(len(embedded_matrix)):
        for j in range(len(embedded_matrix)):
            distances[i][j] = np.linalg.norm(embedded_matrix[i] - embedded_matrix[j])

    print(distances)
    # Побудова рекурентної карти
    plt.imshow(distances, cmap="gray", origin="lower")
    plt.title("Рекурентна карта")
    plt.xlabel("Часова точка")
    plt.ylabel("Часова точка")
    plt.colorbar(label="Відстань")
    plt.show()


def plot_ecg():
    def generate_ecg_like_signal(length=1000, heart_rate=60, noise_level=0.1):
        # Генерування основного сигналу серцевого ритму (пульсу)
        t = np.linspace(0, 1, length)
        pulse = np.sin(2 * np.pi * heart_rate * t)

        # Додавання шуму
        noise = np.random.normal(scale=noise_level, size=length)
        ecg_like_signal = pulse + noise

        return ecg_like_signal

    # Параметри для генерації сигналу
    length = 1000  # Довжина часового ряду
    heart_rate = 60  # Серцевий ритм в ударах на хвилину (приблизно)
    noise_level = 0.1  # Рівень шуму в сигналі

    # Генерування сигналу
    ecg_data = generate_ecg_like_signal(length, heart_rate, noise_level)
    phasespace(ecg_data)
    crp(ecg_data)


def plot_economic():
    def generate_economic_data(length=1000, initial_value=100, volatility=0.1):
        # Генерація випадкових змін
        random_changes = volatility * np.random.randn(length)

        # Ініціалізація часового ряду
        economic_data = np.zeros(length)
        economic_data[0] = initial_value

        # Генерація економічного часового ряду
        for t in range(1, length):
            economic_data[t] = economic_data[t - 1] + random_changes[t]

        return economic_data

    # Параметри генерації даних
    data_length = 1000  # Довжина часового ряду
    initial_value = 100  # Початкове значення
    volatility = 0.1  # Волатильність (рівень змінності)

    # Згенерувати економічні дані
    economic_data = generate_economic_data(data_length, initial_value, volatility)
    # Приклад економічного часового ряду (випадкові значення)
    phasespace(economic_data)
    crp(economic_data)


def plot_seismic():
    def generate_seismic_data(length=100, frequency=1, noise_level=0.1):
        t = np.arange(length)
        seismic_signal = np.sin(2 * np.pi * frequency * t / length)
        noise = noise_level * np.random.randn(length)
        seismic_data = seismic_signal + noise
        return seismic_data

    # Параметри генерації даних
    data_length = 100  # Довжина часового ряду
    signal_frequency = 5  # Частота сигналу
    noise_level = 0.2  # Рівень шуму

    # Згенерувати сейсмічні дані
    seismic_data = generate_seismic_data(data_length, signal_frequency, noise_level)
    phasespace(seismic_data)
    crp(seismic_data)


def plot_eeg():
    def generate_eeg_data(
        length=1000, frequencies=[10, 20, 30], amplitudes=[1, 0.5, 0.3], noise_level=0.1
    ):
        # Генерація часу
        t = np.arange(length)

        # Генерація сигналу ЕЕГ
        eeg_data = np.zeros(length)
        for freq, amp in zip(frequencies, amplitudes):
            eeg_data += amp * np.sin(2 * np.pi * freq * t / length)

        # Додавання шуму
        noise = noise_level * np.random.randn(length)
        eeg_data += noise

        return eeg_data

    # Параметри генерації даних
    data_length = 1000  # Довжина часового ряду
    frequencies = [10, 20, 30]  # Частоти сигналу
    amplitudes = [1, 0.5, 0.3]  # Амплітуди сигналу
    noise_level = 0.1  # Рівень шуму

    # Згенерувати дані для ЕЕГ
    eeg_data = generate_eeg_data(data_length, frequencies, amplitudes, noise_level)
    phasespace(eeg_data)
    crp(eeg_data)


def plot_profitability():
    def generate_profitability_data(length=1000, initial_value=100, volatility=0.1):
        # Генерація випадкових змін прибутковості
        random_changes = volatility * np.random.randn(length)

        # Ініціалізація часового ряду
        profitability_data = np.zeros(length)
        profitability_data[0] = initial_value

        # Генерація часового ряду прибутковості
        for t in range(1, length):
            profitability_data[t] = profitability_data[t - 1] * (1 + random_changes[t])

        return profitability_data

    # Параметри генерації даних
    data_length = 1000  # Довжина часового ряду
    initial_value = 100  # Початкове значення
    volatility = 0.1  # Волатильність (рівень змінності)

    # Згенерувати дані для часового ряду прибутковості
    profitability_data = generate_profitability_data(
        data_length, initial_value, volatility
    )
    phasespace(profitability_data)
    crp(profitability_data)


root = tk.Tk()
root.title("Фазовий портрет та рекурентна карта")

ecg_button = ttk.Button(root, text="Електрокардіограма", command=plot_ecg)
economic_button = ttk.Button(
    root, text="Економічний часовий ряд", command=plot_economic
)
seismic_button = ttk.Button(root, text="Сейсмічний часовий ряд", command=plot_seismic)
eeg_button = ttk.Button(root, text="Енцефалографічний часовий ряд", command=plot_eeg)
profitability_button = ttk.Button(
    root, text="Ряд прибутковості", command=plot_profitability
)

ecg_button.pack(pady=5)
economic_button.pack(pady=5)
seismic_button.pack(pady=5)
eeg_button.pack(pady=5)
profitability_button.pack(pady=5)

root.mainloop()
