import numpy as np
import matplotlib.pyplot as plt
import random

def find_BMU(SOM, x):
    distSq = np.sum(np.square(SOM - x), axis=2)  # Обчислюємо квадрат відстані між кожним нейроном і вхідним вектором
    return np.unravel_index(np.argmin(distSq, axis=None), distSq.shape)  # Повертаємо індекс нейрона з найменшою відстанню
    
def update_weights(SOM, train_ex, learn_rate, radius_sq, BMU_coord, step=3):
    g, h = BMU_coord
    if radius_sq < 1e-3: 
        SOM[g,h,:] += learn_rate * (train_ex - SOM[g,h,:]) # Оновлюємо ваги для BMU 
        return SOM 
    for i in range(max(0, g-step), min(SOM.shape[0], g+step)): 
        for j in range(max(0, h-step), min(SOM.shape[1], h+step)): 	
            dist_sq = np.square(i - g) + np.square(j - h) # Обчислюємо квадрат відстані між BMU і поточним нейроном
            dist_func = np.exp(-dist_sq / 2 / radius_sq) # Обчислюємо функцію відстані для поточного нейрона 
            SOM[i,j,:] += learn_rate * dist_func * (train_ex - SOM[i,j,:]) # Оновлюємо ваги для поточного нейрона   
    return SOM 

def train_SOM(SOM, train_data, learn_rate=0.1, radius_sq=1, 
lr_decay=0.1, radius_decay=0.1, epochs=10):  
    learn_rate_0 = learn_rate # Початкове значення швидкості навчання
    radius_0 = radius_sq # Початкове значення радіусу
    for epoch in range(epochs):  
        random.shuffle(train_data) # Перемішуємо тренувальні дані на початку кожної епохи     
        for train_ex in train_data:   
            g, h = find_BMU(SOM, train_ex) # Знаходимо BMU для кожного прикладу 
            SOM = update_weights(SOM, train_ex, learn_rate, radius_sq, (g,h)) # Оновлюємо ваги нейронів
        learn_rate = learn_rate_0 * np.exp(-epoch * lr_decay) # Оновлюємо швидкість навчання 
        radius_sq = radius_0 * np.exp(-epoch * radius_decay) # Оновлюємо радіус            
    return SOM

m = 10  
n = 10
n_x = 3000
rand = np.random.RandomState(0)
train_data = rand.randint(0, 255, (n_x, 3))
SOM = rand.randint(0, 255, (m, n, 3)).astype(float)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 3.5), 
                        subplot_kw=dict(xticks=[], yticks=[])) 
ax[0].imshow(train_data.reshape(50, 60, 3))
ax[0].set_title('Training Data')
ax[1].imshow(SOM.astype(int))
ax[1].set_title('Randomly Initialized SOM Grid')

plt.show()
