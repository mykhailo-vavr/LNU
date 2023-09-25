import statistics
from cmath import sqrt
import numpy as np
import collections
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import pandas as pd
from scipy.stats import moment
from scipy.stats import skew
from scipy.stats import kurtosis


def variation(standart, selective_average):
    variation = standart / selective_average
    print("Варіація: ", variation)
    return variation


def selective_despercy(deviation, n):
    selective_despercy = deviation / n
    return selective_despercy


def sample_standard_deviation(selective_despercy):
    sample_standard_deviation = sqrt(selective_despercy)
    print("Вибіркове середньо-квадратичне відхилення: ",
          sample_standard_deviation)
    return sample_standard_deviation


def table(array):
    data = pd.Series(array)
    table = data.value_counts(sort=False)
    return table


def swing(array):
    swing = max(array) - min(array)
    return swing


def interquartile_range(frequency, array):
    variation_series = np.sort(array)
    step_quartile = int(sum(frequency) / 4)
    step_octil = int(sum(frequency) / 8)
    step_decil = int(sum(frequency) / 10)
    step_cintul = int(sum(frequency) / 100)
    quartils = []
    octils = []
    decils = []
    cintuls = []
    if sum(frequency) % 4 == 0:
        for q in range(1, 4):
            quartil = (variation_series[q * step_quartile - 1])
            quartils.append(quartil)
        interquartile_latitude = quartils[2] - quartils[0]
        print("Квартиль", *quartils)
    if sum(frequency) % 8 == 0:
        for o in range(1, 8):
            octil = (variation_series[o * step_octil - 1])
            octils.append(octil)
        interoctile_latitude = octils[6] - octils[0]
        print("Октиль", *octils)
    if sum(frequency) % 10 == 0:
        for d in range(1, 10):
            decil = (variation_series[d * step_decil - 1])
            decils.append(decil)
        interdecile_latitude = decils[8] - decils[0]
        print("Дециль", *decils)
    if sum(frequency) % 100 == 0:
        for c in range(1, 100):
            cintul = (variation_series[c * step_cintul - 1])
            cintuls.append(cintul)
        intercentile_latitude = cintuls[98] - cintuls[0]
        print("Інтерцентильна широта:", intercentile_latitude)
        print("Центиль", *cintuls)


def empireFunc(array_of_keys, array_of_probability):
    x_table = {0: 'x < ' + str(array_of_keys[0])}
    i = 0
    temp = 0
    while i < len(array_of_keys) - 1:
        string = str(array_of_keys[i]) + " <= x < " + str(array_of_keys[i + 1])
        temp += array_of_probability[i]
        x_table.update({np.around(temp, 2): string})
        i += 1

    x_table.update({1: 'x>=' + str(array_of_keys[i])})

    table = PrettyTable(['', 'x'])
    table.add_rows(x_table.items())
    table.vrules = 2
    table.hrules = 2
    print(table)


def vizualizeEmpireFunc(array_of_keys, array):
    delta = 2
    i = 0
    temp = 0
    plt.hlines(temp, array_of_keys[i] - delta, array_of_keys[i])
    while i < len(array_of_keys) - 1:
        temp += array[i]
        plt.hlines(temp, array_of_keys[i], array_of_keys[i + 1])
        i += 1

    plt.hlines(1, array_of_keys[-1], array_of_keys[-1] + delta)
    plt.xlim(-delta, array_of_keys[-1] + delta)
    plt.ylim(0, 1.5)

    plt.grid()
    plt.show()


def probabilityFrequency(array, n):
    probabilities = [np.around(value / n, 2) for value in array]
    return probabilities


def printtable_prob(element, probabilities):
    table = PrettyTable()
    table.add_row(element)
    table.add_row(probabilities)
    table.vrules = 2
    table.hrules = 2
    print(table)
    # for i in range(len(element)):
    #     print(element[i], " - ", probabilities[i])


def mode(array):
    vals, counts = np.unique(array, return_counts=True)
    mode_value = np.argwhere(counts == np.max(counts))
    print("Мода = ", *vals[mode_value].flatten().tolist())
    return vals[mode_value].flatten().tolist()


def mediana(array):
    mediana = statistics.median(array)
    print("Медіана: ", mediana)
    return mediana


def selective_average(array):
    mean = statistics.mean(array)
    print("Середнє вибіркове: ", mean)
    return mean


def deviation(elem_array, freq_array, selective_average):
    dev = 0
    for i, j in zip(freq_array, elem_array):
        dev += (i * ((j - selective_average)**2))
    return dev


def variance(array):
    print("Варіанса: ", statistics.variance(array))
    return statistics.variance(array)


def standart(array):
    print("Стандарт: ", statistics.stdev(array))
    return statistics.stdev(array)


def moments_stat_material(array):
    m1 = statistics.mean(array)
    print("Початковий момент: ", m1)
    print("Другий центральний момент: ", moment(array, moment=2))
    print("Третій центральний момент: ", moment(array, moment=3))
    print("Четвертий центральний момент: ", moment(array, moment=4))


def threeMoment(freq, element, average, n):
    dev = 0
    for key, val in zip(element, freq):
        dev += val * np.power((key - average), 3)
    return np.round(dev / n, 2)


def asymmetry(array):
    print("Асиметрія: ", skew(array))


def exces(array):
    print("Ексцес: ", kurtosis(array, fisher=True))


def interval_distribution(array):
    sample_size = len(array)
    length_of_the_sample = max(array) - min(array)
    print("Об'єм вибірки: ", sample_size)
    print("Довжина проміжку: ", round(length_of_the_sample, 3))


def countNumberInList(array, first, second, first_):
    count = 0
    if first_:
        for value in array:
            if first <= value <= second:
                count += 1
        return count
    for value in array:
        if first < value <= second:
            count += 1
    return count


def interval_mater(array):
    i = 0
    while not (np.power(2, i) < len(array) <= np.power(2, i + 1)):
        i += 1

    i += 1
    step = (max(array) - min(array)) / i
    first = array[0]
    tabl = {}
    for_plt = {}
    ranges = {}
    for value in range(i):
        if (value == 0):
            tabl.update({
                f"[{np.round(first, 2)}-{np.round(first + step, 2)}]":
                (countNumberInList(array, first, first + step, True))
            })
            for_plt.update(
                {first: (countNumberInList(array, first, first + step, True))})
            ranges.update({
                (first, first + step):
                countNumberInList(array, first, first + step, True)
            })
        else:
            tabl.update({
                f"({np.round(first, 2)}-{np.round(first + step, 2)}]":
                countNumberInList(array, first, first + step, False)
            })
            for_plt.update(
                {first: countNumberInList(array, first, first + step, False)})
            ranges.update({
                (first, first + step):
                countNumberInList(array, first, first + step, False)
            })
        first += step

    print("Інтервальний розподіл: ")
    table = PrettyTable()
    table.add_row(tabl.keys())
    table.add_row(tabl.values())
    table.vrules = 2
    table.hrules = 2
    print(table)

    for_plt.update(
        {first: countNumberInList(array, first, first + step, False)})
    plt.xticks(list(for_plt.keys()))
    plt.hist(for_plt.keys(),
             bins=list(for_plt.keys()),
             weights=for_plt.values(),
             edgecolor='black')
    plt.title('Гістограма розподілу')
    plt.show()

    return for_plt, step, ranges


def serednie(variation_series, val, step):
    first, sum = variation_series[0], 0

    for i in val.values():
        sum += i * first
        first += step

    return sum / len(variation_series)


def moda_for_interval(frequency_for_interval):
    n_previous = 0
    nmod = list(frequency_for_interval.values())[0]
    hmodstart = list(frequency_for_interval.keys())[0]
    hmodend = list(frequency_for_interval.keys())[1]

    i = 1
    while i < len(frequency_for_interval.keys()) - 1:
        if list(frequency_for_interval.values())[i] > nmod:
            n_previous = list(frequency_for_interval.values())[i - 1]
            nmod = list(frequency_for_interval.values())[i]
            hmodstart = list(frequency_for_interval.keys())[i + 1]
            hmodend = list(frequency_for_interval.keys())[i + 1]
        i += 1

    try:
        nmod_next = list(frequency_for_interval.values())[i]
    except:
        nmod_next = list(frequency_for_interval.values())[i - 1]
    mod = hmodstart + (
        (nmod - n_previous) /
        (nmod - n_previous + nmod - nmod_next)) * (hmodend - hmodstart)
    return mod


def printMedian(frequency_for_interval):
    count_freq = sum(frequency_for_interval.values())
    m = 0
    for f in frequency_for_interval.values():
        if m + f < count_freq / 2:
            m += f
        else:
            break

    count = 0
    for i in frequency_for_interval.values():
        count += i

    i = 0
    n = 0

    while n < count / 2:
        n += list(frequency_for_interval.values())[i]
        i += 1
    i -= 1
    hstart = list(frequency_for_interval.keys())[i]
    try:
        hend = list(frequency_for_interval.keys())[i + 1]
    except:
        hend = hstart
    n = list(frequency_for_interval.values())[i]
    med = hstart + ((hend - hstart) / n) * ((count_freq / 2) - m)
    return med


def deviacia_for_interval(range, serednie):
    sum = 0
    for key, value in range.items():
        (start, end) = key
        med = (end + start) / 2
        sum += value * np.power((serednie - med), 2)
    return sum


def varianca_intrl(dev, size):
    varianca = np.round(dev / (size - 1), 2)
    return varianca


def standart_for_interval(varianca):
    return np.round(np.power(varianca, 1 / 2), 2)


def variacia_for_interval(standart, serednie):
    return np.round(standart / serednie, 2)


def despercia(dev, size):
    return dev / size


def rozmah_intrl(range):
    first = list(range.keys())[0]
    last = list(range.keys())[-1]
    first_f, first_e = first
    last_f, last_e = last
    return np.round((last_e - first_f), 2)


def three_centralni_moment(ranges, serednie, size):
    sum = 0
    for key, value in ranges.items():
        (start, end) = key
        med = (end + start) / 2
        sum += value * np.power((med - serednie), 3)

    return sum / size


def central_m(ranges, serednie, size):
    sum = 0
    for key, value in ranges.items():
        (start, end) = key
        med = (end + start) / 2
        sum += value * np.power((med - serednie), 4)

    return sum / size


# -------------- #
#
#   Show
#
# -------------- #

a = int(input("початок "))
b = int(input("кінцева "))
c = int(input("розмір "))
array = np.random.randint(a, high=b + 1, size=c)

element = np.unique(array)
freq = []

counter = collections.Counter(array)
for a in element:
    count = counter[a]
    freq.append(count)

print("Вибірка")
print(*array)
print()

print("Варіаційний ряд")
variation_array = np.sort(array)
print(*variation_array)
print()

print("Частотна таблиця")
df = table(variation_array)
print(df)

df.plot(label='Частота елементів')
plt.legend()
plt.show()

df.plot.bar(label='Частота елементів')
plt.legend()
plt.show()

prob = probabilityFrequency(freq, len(array))
print("Таблиця ймовірностей")
printtable_prob(element, prob)

print(empireFunc(element, prob))
vizualizeEmpireFunc(element, prob)
print()
mode(array)
mediana(array)
selective_average = selective_average(array)
print()
dev = deviation(element, freq, statistics.mean(array))
print("Девіація: ", dev)
variance(array)
standart(array)
variation(statistics.stdev(array), statistics.mean(array))
selective_despercy = selective_despercy(dev, len(array))
print("Вибіркова дисперсія: ", selective_despercy)
sample_standard_deviation(selective_despercy)
print("Розмах: ", swing(array))
print()
print("Інтерквантильні широти: ")
interquartile_range(freq, array)
print()
print("Моменти статистичного матеріалу: ")
moments_stat_material(array)
print("Статистики форми: ")
asymmetry(array)
exces(array)





_intrv, step, ranges = interval_mater(variation_array)
ser = serednie(variation_array, _intrv, step)
print()
print()

print("Середнє вибіркове : ", ser)
print("Мода для інтервального: ", moda_for_interval(_intrv))
print("Медіана для інтервального: ", printMedian(_intrv))

deviacia = deviacia_for_interval(ranges, ser)
print("Девіація", deviacia)
varianca_int = varianca_intrl(deviacia, len(variation_array))
print("Варіанса: ", varianca_int)
standart = standart_for_interval(varianca_int)
print("Стандарт: ", standart)
print("Варіація: ", variacia_for_interval(standart, ser))

vub_desp = despercia(deviacia, len(variation_array))
print("Вибіркова дисперсія: ", vub_desp)
print("Вибіркове середнє квадратичне відхилення: " +
      str(np.round(np.power(vub_desp, 1 / 2), 2)))
print("Розмах: ", rozmah_intrl(ranges))

three_central_moment = three_centralni_moment(ranges, ser,
                                              len(variation_array))
four_central_moment = central_m(ranges, ser, len(variation_array))

print("Асиметрія: ", three_central_moment / (np.power(vub_desp, (3 / 2))))
print("Ексцес: ", (four_central_moment / (np.power(varianca_int, 2)) - 3))

print("Початковий момент: ", ser)
print("Другий центральний момент: ", varianca_int)
print("Третій центральний момент: ", three_central_moment)
print("Четвертий центральний момент: ", four_central_moment)