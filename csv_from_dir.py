import os
import csv

# Папки з зображеннями
cars = r'C:\Users\PC\PycharmProjects\for_datasets\photos\cars'
no_cars = r'C:\Users\PC\PycharmProjects\for_datasets\photos\no_cars'

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
csv_file = 'dataset.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['image_path', 'label'])  # Заголовки стовпців
    writer.writerows(all_images)
