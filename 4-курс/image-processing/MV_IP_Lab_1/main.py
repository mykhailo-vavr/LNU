import numpy as np
from PIL import Image
import os
import time

# Шлях до початкового 24-бітного BMP файлу
bmp_path = "sample.bmp"

# Завантаження зображення

original_image = Image.open(bmp_path)

save_folder = "ToSave"

# 1. Збереження у форматі BMP (RLE)
bmp_rle_path = os.path.join(save_folder, "Image_rle.bmp")
start_time = time.time()
original_image.save(bmp_rle_path, format="BMP", compression="RLE")
end_time = time.time()
bmp_rle_size = os.path.getsize(bmp_rle_path)

print(f"1. Збережено зображення у форматі BMP (RLE) в папці ToSave:")
print(
    f"   Час збереження: {end_time - start_time:.4f} сек."
)  # Виводимо 4 знаки після коми
print(f"   Розмір файлу: {bmp_rle_size / 1024:.2f} KB\n")

# 2. Збереження у форматі TIFF (LZW)
tiff_path = os.path.join(save_folder, "Image_lzw.tiff")
start_time = time.time()
original_image.save(tiff_path, format="TIFF", compression="LZW")
end_time = time.time()
tiff_size = os.path.getsize(tiff_path)

print(f"2. Збережено зображення у форматі TIFF (LZW) в папці ToSave:")
print(f"   Час збереження: {end_time - start_time:.4f} сек.")
print(f"   Розмір файлу: {tiff_size / 1024:.2f} KB\n")

# 3. Збереження у форматі JPEG
jpeg_path = os.path.join(save_folder, "Image.jpg")
start_time = time.time()
original_image.save(jpeg_path, format="JPEG", quality=100)
end_time = time.time()
jpeg_size = os.path.getsize(jpeg_path)

print(f"3. Збережено зображення у форматі JPEG в папці ToSave:")
print(f"   Час збереження: {end_time - start_time:.4f} сек.")
print(f"   Розмір файлу: {jpeg_size / 1024:.2f} KB\n")


# 2 пункт
# для jpeg
jpeg_path = "ToSave//Image.jpg"
jpeg_image = Image.open(jpeg_path)

# Перетворюємо зображення у масиви NumPy
original_array = np.array(original_image)
jpeg_array = np.array(jpeg_image)

# 1. Віднімання для всіх кольорів разом
difference_all_colors = (
    original_array - jpeg_array
)  # Віднімаємо значень пікселів оригінального зображення від значень пікселів зображення у форматі JPEG
difference_all_colors_image = Image.fromarray(
    np.uint8(difference_all_colors)
)  # конвертуємо назад в зображення
difference_all_colors_path = save_folder + "/all_colors_difference_jpeg.bmp"
difference_all_colors_image.save(difference_all_colors_path)

# 2. Віднімання для кожного кольору окремо (R, G, B)
difference_R = original_array.copy()
difference_R[:, :, 1:3] = 0  # Обнулити G та B
difference_R = difference_R - jpeg_array

difference_G = original_array.copy()
difference_G[:, :, 0] = 0  # Обнулити R та В
difference_G[:, :, 2] = 0
difference_G = difference_G - jpeg_array

difference_B = original_array.copy()
difference_B[:, :, 0:2] = 0  # Обнулити R та G
difference_B = difference_B - jpeg_array

# Збереження зображень
difference_R_image = Image.fromarray(np.uint8(difference_R))  # конвертуємо в зображення
difference_R_path = save_folder + "/difference_R_for_jpeg.bmp"
difference_R_image.save(difference_R_path)

difference_G_image = Image.fromarray(np.uint8(difference_G))
difference_G_path = save_folder + "/difference_G_for_jpeg.bmp"
difference_G_image.save(difference_G_path)

difference_B_image = Image.fromarray(np.uint8(difference_B))
difference_B_path = save_folder + "/difference_B_for_jpeg.bmp"
difference_B_image.save(difference_B_path)


# різниці між пікселями оригінального та відтисненого зображення. Якщо значення пікселя дорівнює 0, це означає, що немає втрати для цього пікселя.
def calculate_loss(image_array, compressed_array):
    return np.abs(image_array - compressed_array)


# Загальні втрати
total_loss = calculate_loss(original_array, jpeg_array)
average_total_loss = np.mean(total_loss)

# Втрати для кожного кольору окремо
loss_R = calculate_loss(original_array[:, :, 0], jpeg_array[:, :, 0])
average_loss_R = np.mean(loss_R)

loss_G = calculate_loss(original_array[:, :, 1], jpeg_array[:, :, 1])
average_loss_G = np.mean(loss_G)

loss_B = calculate_loss(original_array[:, :, 2], jpeg_array[:, :, 2])
average_loss_B = np.mean(loss_B)

print(f"\n\nЗагальні втрати для jpeg: {average_total_loss}")
print(f"Втрати для R для jpeg: {average_loss_R}")
print(f"Втрати втрати для G для jpeg: {average_loss_G}")
print(f"Втрати втрати для B для jpeg: {average_loss_B}")


# для bmp
bmp_path = "ToSave//Image_rle.bmp"
bmp_image = Image.open(bmp_path)

# Перетворюємо зображення у масиви NumPy
bmp_array = np.array(bmp_image)

# 1. Віднімання для всіх кольорів разом
difference_all_colors = (
    original_array - bmp_array
)  # Віднімаємо значень пікселів оригінального зображення від значень пікселів зображення у форматі JPEG
difference_all_colors_image = Image.fromarray(
    np.uint8(difference_all_colors)
)  # конвертуємо назад в зображення
difference_all_colors_path = save_folder + "/all_colors_difference_bmp.bmp"
difference_all_colors_image.save(difference_all_colors_path)

# 2. Віднімання для кожного кольору окремо (R, G, B)
difference_R = original_array.copy()
difference_R[:, :, 1:3] = 0  # Обнулити G та B
difference_R = difference_R - bmp_array

difference_G = original_array.copy()
difference_G[:, :, 0] = 0  # Обнулити R та В
difference_G[:, :, 2] = 0
difference_G = difference_G - bmp_array

difference_B = original_array.copy()
difference_B[:, :, 0:2] = 0  # Обнулити R та G
difference_B = difference_B - bmp_array

# Збереження зображень
difference_R_image = Image.fromarray(np.uint8(difference_R))  # конвертуємо в зображення
difference_R_path = save_folder + "/difference_R_for_bmp.bmp"
difference_R_image.save(difference_R_path)

difference_G_image = Image.fromarray(np.uint8(difference_G))
difference_G_path = save_folder + "/difference_G_for_bmp.bmp"
difference_G_image.save(difference_G_path)

difference_B_image = Image.fromarray(np.uint8(difference_B))
difference_B_path = save_folder + "/difference_B_for_bmp.bmp"
difference_B_image.save(difference_B_path)


# Загальні втрати
total_loss = calculate_loss(original_array, bmp_array)
average_total_loss = np.mean(total_loss)

# Втрати для кожного кольору окремо
loss_R = calculate_loss(original_array[:, :, 0], bmp_array[:, :, 0])
average_loss_R = np.mean(loss_R)

loss_G = calculate_loss(original_array[:, :, 1], bmp_array[:, :, 1])
average_loss_G = np.mean(loss_G)

loss_B = calculate_loss(original_array[:, :, 2], bmp_array[:, :, 2])
average_loss_B = np.mean(loss_B)

print(f"\n\nЗагальні втрати для bmp: {average_total_loss}")
print(f"Втрати для R для bmp: {average_loss_R}")
print(f"Втрати для G для bmp: {average_loss_G}")
print(f"Втрати для B для bmp: {average_loss_B}")


# для tiff
tiff_path = "ToSave//Image_lzw.tiff"
tiff_image = Image.open(tiff_path)

# Перетворюємо зображення у масиви NumPy
tiff_array = np.array(tiff_image)

# 1. Віднімання для всіх кольорів разом
difference_all_colors = (
    original_array - tiff_array
)  # Віднімаємо значень пікселів оригінального зображення від значень пікселів зображення у форматі JPEG
difference_all_colors_image = Image.fromarray(
    np.uint8(difference_all_colors)
)  # конвертуємо назад в зображення
difference_all_colors_path = save_folder + "/all_colors_difference_tiff.bmp"
difference_all_colors_image.save(difference_all_colors_path)

# 2. Віднімання для кожного кольору окремо (R, G, B)
difference_R = original_array.copy()
difference_R[:, :, 1:3] = 0  # Обнулити G та B
difference_R = difference_R - tiff_array

difference_G = original_array.copy()
difference_G[:, :, 0] = 0  # Обнулити R та В
difference_G[:, :, 2] = 0
difference_G = difference_G - tiff_array

difference_B = original_array.copy()
difference_B[:, :, 0:2] = 0  # Обнулити R та G
difference_B = difference_B - tiff_array

# Збереження зображень
difference_R_image = Image.fromarray(np.uint8(difference_R))  # конвертуємо в зображення
difference_R_path = save_folder + "/difference_R_for_tiff.bmp"
difference_R_image.save(difference_R_path)

difference_G_image = Image.fromarray(np.uint8(difference_G))
difference_G_path = save_folder + "/difference_G_for_tiff.bmp"
difference_G_image.save(difference_G_path)

difference_B_image = Image.fromarray(np.uint8(difference_B))
difference_B_path = save_folder + "/difference_B_for_tiff.bmp"
difference_B_image.save(difference_B_path)


# Загальні втрати
total_loss = calculate_loss(original_array, tiff_array)
average_total_loss = np.mean(total_loss)

# Втрати для кожного кольору окремо
loss_R = calculate_loss(original_array[:, :, 0], tiff_array[:, :, 0])
average_loss_R = np.mean(loss_R)

loss_G = calculate_loss(original_array[:, :, 1], tiff_array[:, :, 1])
average_loss_G = np.mean(loss_G)

loss_B = calculate_loss(original_array[:, :, 2], tiff_array[:, :, 2])
average_loss_B = np.mean(loss_B)

print(f"\n\nЗагальні втрати для tiff: {average_total_loss}")
print(f"Втрати для R для tiff: {average_loss_R}")
print(f"Втрати для G для tiff: {average_loss_G}")
print(f"Втрати для B для tiff: {average_loss_B}")
