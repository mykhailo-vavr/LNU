import numpy as np
import matplotlib.pyplot as plt


def euclidean_distance(point1, point2):
    """Обчислює відстань між двома точками за формулою Евкліда."""
    return np.linalg.norm(point1 - point2)


def find_neighbors(data, point_index, eps):
    """Знаходить всі точки в наборі даних, розташовані на відстані eps від заданої точки."""
    neighbors = []
    for i, point in enumerate(data):
        if euclidean_distance(data[point_index], point) <= eps:
            neighbors.append(i)
    return neighbors


def dbscan(data, eps, min_samples):
    """
    Алгоритм DBSCAN для кластеризації.

    Параметри:
    - data: Вхідні точки даних
    - eps: Максимальна відстань між двома точками, щоб вони вважалися сусідніми
    - min_samples: Мінімальна кількість точок, необхідних для формування щільної області

    Повертає:
    - labels: Мітки кластерів для кожної точки даних
    """
    labels = np.zeros(
        len(data)
    )  # Ініціалізуємо мітки кластерів, 0 означає некласифіковано

    cluster_id = 0
    for i, point in enumerate(data):
        if labels[i] != 0:  # Пропускаємо точки, які вже віднесені до кластера
            continue

        neighbors = find_neighbors(data, i, eps)

        if len(neighbors) < min_samples:
            labels[i] = -1  # Позначаємо як шум
        else:
            cluster_id += 1
            labels[i] = cluster_id
            expand_cluster(data, labels, neighbors, cluster_id, eps, min_samples)

    return labels


def expand_cluster(data, labels, neighbors, cluster_id, eps, min_samples):
    """
    Розширення кластера для включення досяжних точок.

    Параметри:
    - data: Вхідні точки даних
    - labels: Мітки кластерів для кожної точки даних
    - point_index: Індекс поточної точки даних
    - neighbors: Індекси сусідніх точок
    - cluster_id: Поточний ідентифікатор кластера
    - eps: Максимальна відстань між двома точками, щоб вони вважалися сусідніми
    - min_samples: Мінімальна кількість точок, необхідна для формування щільної області
    """
    for neighbor_index in neighbors:
        if labels[neighbor_index] == -1:  # Шумові точки можна віднести до кластера
            labels[neighbor_index] = cluster_id
        elif labels[neighbor_index] == 0:  # Некласифіковані точки
            labels[neighbor_index] = cluster_id
            neighbor_neighbors = find_neighbors(data, neighbor_index, eps)
            if len(neighbor_neighbors) >= min_samples:
                neighbors.extend(neighbor_neighbors)


def plot_clusters(data, labels):
    """
    Візуалізує кластеризовані дані.

    Параметри:
    - data: Вхідні точки даних
    - labels: Мітки кластерів для кожної точки даних
    """
    unique_labels = np.unique(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    for i, label in enumerate(unique_labels):
        if label == -1:
            color = "k"  # Шумові точки у чорному кольорі
        else:
            color = colors[i]

        cluster_points = data[labels == label]
        plt.scatter(
            cluster_points[:, 0],
            cluster_points[:, 1],
            color=color,
            label=f"Кластер {int(label)}",
        )

    plt.title("Кластеризація методом DBSCAN")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


# Приклад використання
if __name__ == "__main__":
    # Генеруємо вибірку даних
    data = np.random.randn(100, 2)

    # Виконуємо кластеризацію методом DBSCAN
    eps = 0.5  # Максимальна відстань між двома точками, щоб вони вважалися сусідніми
    min_samples = (
        5  # Мінімальна кількість точок, необхідна для формування щільної області
    )

    labels = dbscan(data, eps, min_samples)

    # Візуалізуємо кластери
    plot_clusters(data, labels)
