import json
import os
import cv2
from ultralytics import YOLO
"""
A function to generate JSON annotations for detected objects in images using YOLO.

Parameters:
- image_path: str, the path to the image file for which to create annotations.
- output_dir: str, the directory where the generated JSON file will be saved.

No return value. The function saves the JSON file with detected objects' annotations in the specified output directory.

Function: process_directory
Processes all images in the given directory and generates JSON files for each detected object.

Parameters:
- input_dir: str, the directory containing input image files.
- output_dir: str, the directory where the output JSON files will be saved.

No return value. The function processes images in input_dir and saves JSON files in output_dir.
"""

# Завантаження моделі YOLO
model = YOLO(r'C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\trainYOLO\yolov8s.pt')  # Вказуємо шлях до вашої моделі

# Функція для передбачення і створення JSON для одного зображення
def generate_json_from_yolo(image_path, output_dir):
    # Виконуємо передбачення
    results = model(image_path)

    # Отримуємо ім'я файлу без розширення
    image_name = os.path.basename(image_path)
    file_name = os.path.splitext(image_name)[0]

    # Зчитуємо зображення, щоб дізнатися його розміри
    img = cv2.imread(image_path)
    image_height, image_width = img.shape[:2]

    # Підготовка структури JSON
    data = {
        "version": "5.4.1",
        "flags": {},
        "shapes": [],
        "imagePath": image_path,
        "imageData": None,
        "imageHeight": image_height,
        "imageWidth": image_width
    }

    # Отримуємо bounding boxes з результатів
    for bbox in results[0].boxes:  # results[0].boxes містить всі об'єкти на першому зображенні
        # Конвертуємо значення координат у звичайні float
        x_min, y_min, x_max, y_max = [float(coord) for coord in bbox.xyxy[0].numpy()]
        label = model.names[int(bbox.cls[0])]  # Отримуємо назву класу об'єкта

        # Фільтруємо тільки автомобілі
        if label == "car":
            # Створюємо структуру "shapes"
            shape = {
                "label": label,
                "points": [
                    [x_min, y_min],  # Ліва верхня точка
                    [x_max, y_max]   # Права нижня точка
                ],
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {},
                "mask": None
            }
            data["shapes"].append(shape)

    # Записуємо результати в JSON файл
    output_file = os.path.join(output_dir, f"{file_name}.json")
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"JSON файл збережено як: {output_file}")

# Функція для обробки всіх зображень у директорії
def process_directory(input_dir, output_dir):
    # Перевіряємо, чи існує директорія з вхідними зображеннями
    if not os.path.exists(input_dir):
        print(f"Директорія {input_dir} не знайдена!")
        return

    # Перевіряємо, чи існує директорія для вихідних файлів, якщо ні — створюємо її
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Проходимося по кожному файлу в директорії
    for file_name in os.listdir(input_dir):
        # Перевіряємо, чи файл є зображенням (можна розширити список форматів)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, file_name)
            generate_json_from_yolo(image_path, output_dir)

# Приклад використання
input_dir = r"C:\Users\PC\PycharmProjects\new video&photo\photo for dataset\cars"  # Директорія з зображеннями
output_dir = r"C:\Users\PC\OneDrive\Робочий стіл\OutputDir"  # Директорія для збереження JSON файлів
process_directory(input_dir, output_dir)
