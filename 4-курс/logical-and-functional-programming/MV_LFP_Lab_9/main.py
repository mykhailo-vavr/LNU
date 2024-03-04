from math import pi

# порівняння з mapcar
# map = mapcar також застовує функцію для кожного елементу
# також має довжину результату таку ж як і вхідний ліст
degrees = [90, 180, 270, 360]
radians = list(map(lambda x: x * (pi / 180.0), degrees))
print(radians)

# Умовна фільтрація з map
less_than_5 = lambda x: x if x < 5 else None

# В пайтоні немає відповідника для mapcan
# тому для фільтрація повинні застосовувати filter
# або зовнішній контейнер для результатів
numbers = [1, 2, 3, 4, 5, 6]
filtered_numbers = list(filter(lambda x: less_than_5(x), numbers))
print(filtered_numbers)
