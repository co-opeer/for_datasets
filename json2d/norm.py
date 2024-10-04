import os
import cv2
import pandas as pd
from tqdm import tqdm

"""
A function to resize images and scale bounding boxes based on the provided CSV file.

Parameters:
- csv_file: str, the path to the CSV file containing image and bounding box coordinates.
- images_dir: str, the directory where the images are located.
- output_dir: str, the directory where the resized images and updated annotations will be saved.
- target_size: tuple, optional, the target size to resize the images (default is (416, 416)).

No return value. The function saves the resized images and updated annotations to the output directory.
"""
# Функція для нормалізації координат рамки
def normalize_coordinates(x_min, y_min, x_max, y_max, orig_width, orig_height):
    x_min_norm = x_min / orig_width
    y_min_norm = y_min / orig_height
    x_max_norm = x_max / orig_width
    y_max_norm = y_max / orig_height
    return x_min_norm, y_min_norm, x_max_norm, y_max_norm

# Функція для зміни розміру зображення і масштабування рамок
def resize_and_normalize_images(csv_file, images_dir, output_dir, target_size=(416, 416)):
    # Зчитування CSV-файлу
    df = pd.read_csv(csv_file)
    os.makedirs(output_dir, exist_ok=True)

    # Ітерація по всіх зображеннях у CSV
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        image_name = row['image_name']
        x_min, y_min, x_max, y_max = row['x_min'], row['y_min'], row['x_max'], row['y_max']

        # Зчитування зображення
        image_path = os.path.join(images_dir, image_name)
        if not os.path.exists(image_path):
            print(f"Зображення {image_path} не знайдено, пропускаю...")
            continue
        image = cv2.imread(image_path)
        orig_height, orig_width = image.shape[:2]

        # Нормалізація координат
        x_min_norm, y_min_norm, x_max_norm, y_max_norm = normalize_coordinates(
            x_min, y_min, x_max, y_max, orig_width, orig_height
        )

        # Зміна розміру зображення до target_size
        image_resized = cv2.resize(image, target_size)
        target_height, target_width = target_size

        # Відновлення координат до нового розміру зображення
        x_min_new = x_min_norm * target_width
        y_min_new = y_min_norm * target_height
        x_max_new = x_max_norm * target_width
        y_max_new = y_max_norm * target_height

        # Збереження зображення та оновлених координат
        new_image_name = f"resized_{image_name}"
        new_image_path = os.path.join(output_dir, new_image_name)
        cv2.imwrite(new_image_path, image_resized)

        # Зберігання нових координат до CSV
        df.loc[_, 'x_min'] = x_min_new
        df.loc[_, 'y_min'] = y_min_new
        df.loc[_, 'x_max'] = x_max_new
        df.loc[_, 'y_max'] = y_max_new
        df.loc[_, 'image_name'] = new_image_name

    # Збереження оновленого CSV-файлу
    df.to_csv(os.path.join(output_dir, 'normalized_annotations.csv'), index=False)
    print("Підготовка даних завершена. Файл 'normalized_annotations.csv' збережено в:", output_dir)

# Приклади використання
csv_file_path = 'output.csv'  # Заміни на шлях до твого CSV-файлу
images_directory = r"C:\Users\PC\PycharmProjects\new video&photo\photo for dataset\cars" # Заміни на шлях до директорії з зображеннями
output_directory = r"C:\Users\PC\PycharmProjects\for_datasets\json2d\normalizePhoto"  # Директорія, куди будуть збережені масштабовані зображення

# Виклик функції для масштабування та нормалізації
resize_and_normalize_images(csv_file_path, images_directory, output_directory)
