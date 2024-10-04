import os
from PIL import Image

"""
Creates a dictionary to store the count of images with different resolutions.

Parameters:
directory (str): The path to the directory containing the images.

Returns:
dict: A dictionary with the count of images for each resolution.
"""
def count_images_by_resolution(directory):
    # Створюємо словник для зберігання кількості зображень з різними розмірами
    resolution_counts = {}

    # Перебираємо всі файли в зазначеній папці
    for filename in os.listdir(directory):
        # Отримуємо повний шлях до файлу
        filepath = os.path.join(directory, filename)

        # Перевіряємо, чи є файл зображенням
        if os.path.isfile(filepath) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Відкриваємо зображення
            with Image.open(filepath) as img:
                # Отримуємо розмір зображення
                resolution = img.size

                # Додаємо розмір до словника, або збільшуємо лічильник, якщо такий розмір вже є
                if resolution in resolution_counts:
                    resolution_counts[resolution] += 1
                else:
                    resolution_counts[resolution] = 1

    # Повертаємо словник з кількістю зображень для кожного розміру
    return resolution_counts


# Використання функції
directory = r"C:\Users\PC\OneDrive\Робочий стіл\photo for dataset\cars"
result = count_images_by_resolution(directory)

# Виводимо результат
for resolution, count in result.items():
    print(f'{count} фото з розміром {resolution[0]}x{resolution[1]}')
