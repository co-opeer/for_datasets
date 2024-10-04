import os
import csv
"""
A function to collect image paths and their corresponding labels from specified directories.

Parameters:
- folder_path: str, the path to the folder containing images.
- label: str, the label to assign to the images in the specified folder.

Returns:
- list: A list of lists, where each inner list contains the image path and its corresponding label.

The script combines images from two folders, `cars` and `no_cars`, labeling them as 'true' and 'false', respectively. It then writes the collected paths and labels to a CSV file.

CSV File Output:
- The output CSV file ('../dataset.csv') will contain two columns: 
  - 'image_path': the path to the image file.
  - 'label': the corresponding label ('true' for images with cars, 'false' for images without cars).
"""

# Папки з зображеннями
cars = r"C:\Users\PC\PycharmProjects\new video&photo\new photo\with_cars"
no_cars = r"C:\Users\PC\PycharmProjects\new video&photo\new photo\without_cars"

# Функція для отримання шляхів до зображень у папці та їх класу
def get_image_paths_and_labels(folder_path, label):
    image_paths = []  # Список шляхів до зображень
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Враховуємо лише файли зображень
            image_paths.append([os.path.join(folder_path, filename), label])
    return image_paths

# Папки з зображеннями
positive_folder = cars
negative_folder = no_cars

# Отримання шляхів до зображень та їх класів
positive_images = get_image_paths_and_labels(positive_folder, 'true')
negative_images = get_image_paths_and_labels(negative_folder, 'false')

# Об'єднання списків
all_images = positive_images + negative_images

# Запис у CSV файл
csv_file = '../dataset.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['image_path', 'label'])  # Заголовки стовпців
    writer.writerows(all_images)
