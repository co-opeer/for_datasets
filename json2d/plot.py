import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os

"""
A function to visualize bounding boxes on images based on the coordinates provided in a CSV file.

Parameters:
- csv_file: str, the path to the CSV file containing the coordinates.
- images_dir: str, the directory where the images are located.

No return value.
"""
# Функція для зчитування даних з CSV та побудови графіків
def visualize_bounding_boxes(csv_file, images_dir):
    # Зчитування CSV-файлу з координатами
    df = pd.read_csv(csv_file)

    # Групування за ім'ям зображення (щоб обробляти всі рамки одного зображення разом)
    grouped = df.groupby('image_name')

    for image_name, group in grouped:
        # Відкриття зображення
        image_path = os.path.join(images_dir, image_name)
        if not os.path.exists(image_path):
            print(f"Зображення {image_path} не знайдено, пропускаю...")
            continue

        image = Image.open(image_path)
        fig, ax = plt.subplots(1)
        ax.imshow(image)

        # Додавання рамок на зображення
        for _, row in group.iterrows():
            x_min, y_min, x_max, y_max = row[['x_min', 'y_min', 'x_max', 'y_max']]

            # Побудова прямокутника для кожної рамки
            width = x_max - x_min
            height = y_max - y_min
            rect = patches.Rectangle((x_min, y_min), width, height, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

        plt.title(f"Bounding boxes for {image_name}")
        plt.show()


# Вказати шлях до CSV-файлу з координатами та директорію з зображеннями
csv_file_path = 'normalized_annotations.csv'  # Заміни на шлях до твого CSV-файлу
images_directory = r"C:\Users\PC\PycharmProjects\for_datasets\json2d\normalizePhoto"  # Заміни на шлях до директорії з зображеннями

# Виклик функції для візуалізації
visualize_bounding_boxes(csv_file_path, images_directory)
