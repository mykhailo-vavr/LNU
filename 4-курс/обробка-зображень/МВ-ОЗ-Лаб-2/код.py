from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

# Вказати шлях до зображення
image_path = "parrots.jpeg"

image = cv2.imread(image_path)
blue_channel, green_channel, red_channel = cv2.split(image)

hist_blue = cv2.calcHist([blue_channel], [0], None, [256], [0, 256])
hist_green = cv2.calcHist([green_channel], [0], None, [256], [0, 256])
hist_red = cv2.calcHist([red_channel], [0], None, [256], [0, 256])

x = np.arange(256)

plt.figure(figsize=(8, 6))
plt.title("Original RGB Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(x, hist_blue.ravel(), color="blue", alpha=0.5, label="Blue Channel")
plt.bar(x, hist_green.ravel(), color="green", alpha=0.5, label="Green Channel")
plt.bar(x, hist_red.ravel(), color="red", alpha=0.5, label="Red Channel")
plt.xlim([0, 256])
plt.legend()
plt.show()


image = cv2.imread(image_path)

blue_channel, green_channel, red_channel = cv2.split(image)

# Equalize histograms for each channel
blue_equalized = cv2.equalizeHist(blue_channel)
green_equalized = cv2.equalizeHist(green_channel)
red_equalized = cv2.equalizeHist(red_channel)

# Merge the equalized channels back into an RGB image
equalized_image = cv2.merge([blue_equalized, green_equalized, red_equalized])

# Calculate histograms for each channel in the equalized image
hist_blue = cv2.calcHist([blue_equalized], [0], None, [256], [0, 256])
hist_green = cv2.calcHist([green_equalized], [0], None, [256], [0, 256])
hist_red = cv2.calcHist([red_equalized], [0], None, [256], [0, 256])

# Create an array of values from 0 to 255 for the x-axis
x = np.arange(256)

# Create a histogram with three color channels in the equalized image
plt.figure(figsize=(8, 6))
plt.title("Equalized RGB Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(x, hist_blue.ravel(), color="blue", alpha=0.5, label="Blue Channel")
plt.bar(x, hist_green.ravel(), color="green", alpha=0.5, label="Green Channel")
plt.bar(x, hist_red.ravel(), color="red", alpha=0.5, label="Red Channel")
plt.xlim([0, 256])
plt.legend()
plt.show()

# Display the original and equalized images
cv2.imshow("Original Image", image)
cv2.imshow("Equalized Image", equalized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Define the Robert's masks
roberts_mask_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
roberts_mask_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)

# Apply the Robert's masks using the cv2.filter2D function
roberts_x = cv2.filter2D(image, -1, roberts_mask_x)
roberts_y = cv2.filter2D(image, -1, roberts_mask_y)

# Compute the magnitude of the gradient
roberts_magnitude = np.sqrt(roberts_x**2 + roberts_y**2)

# Display the original image and Robert's gradient magnitude
plt.figure(figsize=(12, 6))
plt.subplot(131), plt.imshow(image, cmap="gray")
plt.title("Original Image"), plt.axis("off")
plt.subplot(132), plt.imshow(roberts_x, cmap="gray")
plt.title("Robert's X"), plt.axis("off")
plt.subplot(133), plt.imshow(roberts_magnitude, cmap="gray")
plt.title("Robert's Magnitude"), plt.axis("off")
plt.show()


# Завантажити зображення за допомогою OpenCV
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Завантажити у відтінках сірого

# Визначити оператори Превіта
previt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)

previt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)

# Застосувати фільтрацію з оператором Превіта для обох напрямків
sobel_x_filtered = cv2.filter2D(image, -1, previt_x)
sobel_y_filtered = cv2.filter2D(image, -1, previt_y)

# Обчислити величину градієнта
sobel_magnitude = np.sqrt(sobel_x_filtered**2 + sobel_y_filtered**2)

# Відобразити оригінальне зображення та результати фільтрації
plt.figure(figsize=(12, 6))
plt.subplot(131), plt.imshow(image, cmap="gray")
plt.title("Оригінальне зображення"), plt.axis("off")
plt.subplot(132), plt.imshow(sobel_x_filtered, cmap="gray")
plt.title("Превіт X"), plt.axis("off")
plt.subplot(133), plt.imshow(sobel_magnitude, cmap="gray")
plt.title("Превіт Magnitude"), plt.axis("off")
plt.show()


# Завантажити зображення за допомогою OpenCV
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Завантажити у відтінках сірого

# Визначити оператори Собела
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# Обчислити величину градієнта
sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Нормалізувати градієнт
sobel_magnitude = cv2.normalize(sobel_magnitude, None, 0, 255, cv2.NORM_MINMAX)

# Відобразити оригінальне зображення та результати фільтрації
plt.figure(figsize=(12, 6))
plt.subplot(131), plt.imshow(image, cmap="gray")
plt.title("Оригінальне зображення"), plt.axis("off")
plt.subplot(132), plt.imshow(sobel_x, cmap="gray")
plt.title("Собель X"), plt.axis("off")
plt.subplot(133), plt.imshow(sobel_magnitude, cmap="gray")
plt.title("Собель Magnitude"), plt.axis("off")
plt.show()
