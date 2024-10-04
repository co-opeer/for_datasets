import json
import csv
import os
"""
A function to resize images and scale bounding boxes based on the provided CSV file.

Parameters:
- csv_file (str): The path to the CSV file containing image filenames and bounding box coordinates (e.g., xmin, ymin, xmax, ymax).
- images_dir (str): The directory where the original images are located.
- output_dir (str): The directory where the resized images and updated annotations will be saved.
- target_size (tuple): Optional; the target size to resize the images. Default is (416, 416).

Returns:
None. The function saves the resized images and updated annotations to the specified output directory.

Detailed Description:
1. **CSV File**: The CSV file should contain columns with image filenames and bounding box coordinates.
2. **Bounding Box Rescaling**: The bounding box coordinates are scaled according to the ratio between the original image size and the `target_size`.
3. **Image Resizing**: Each image is resized to `target_size` using a standard interpolation method.
4. **Output**: Resized images and a new CSV file with updated bounding box coordinates are saved in the `output_dir`.

Example Usage:
```python
resize_and_scale_bounding_boxes(
    csv_file='annotations.csv',
    images_dir='images/',
    output_dir='resized_images/',
    target_size=(416, 416)
)
```
"""

# Функція для обробки кожного JSON-файлу
def process_json_file(file_path, writer):
    with open(file_path, 'r') as f:
        data = json.load(f)

    image_path = data["imagePath"]
    image_name = os.path.basename(image_path)
    shapes = data["shapes"]

    for shape in shapes:
        if shape["label"] == "car" and shape["shape_type"] == "rectangle":
            # Впорядкування координат
            x1, y1 = shape["points"][0]
            x2, y2 = shape["points"][1]

            # Визначення мінімальних та максимальних координат
            x_min, x_max = (x1, x2) if x1 < x2 else (x2, x1)
            y_min, y_max = (y1, y2) if y1 < y2 else (y2, y1)

            # Запис координат у файл CSV
            writer.writerow([image_name, x_min, y_min, x_max, y_max])


# Функція для обробки всіх JSON-файлів у директорії
def process_all_json_files(directory):
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Запис заголовків
        writer.writerow(['image_name', 'x_min', 'y_min', 'x_max', 'y_max'])

        # Перебір усіх файлів у директорії
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                process_json_file(file_path, writer)

    print(f"Всі JSON-файли з директорії {directory} оброблено. Координати збережено у файл output.csv.")


# Вказати шлях до директорії з JSON-файлами
directory_path = r"C:\Users\PC\OneDrive\Робочий стіл\OutputDir"  # Заміни на шлях до твоєї директорії
process_all_json_files(directory_path)
