import os
import shutil
import random
import string

"""
A function that moves files from the source directory to the destination directory.
It retrieves a list of files in the source directory, then iterates through each file,
checking if a file with the same name already exists in the destination directory.
If the file exists, it generates a new name and moves the file with the new name.
If the file does not exist, it simply moves the file to the destination directory.
"""
def move_files(source_dir, destination_dir):
    # Отримання списку файлів у директорії source_dir
    files = os.listdir(source_dir)

    # Переміщення кожного файлу у destination_dir
    for file in files:
        source_path = os.path.join(source_dir, file)
        destination_path = os.path.join(destination_dir, file)

        # Перевірка, чи існує вже файл з такою назвою у destination_dir
        if os.path.exists(destination_path):
            # Якщо файл існує, генеруємо нову назву
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            new_destination_path = os.path.join(destination_dir, random_name + "_" + file)
            # Переміщення файлу з новою назвою
            shutil.move(source_path, new_destination_path)
        else:
            # Якщо файлу з такою назвою ще немає, просто переміщуємо його
            shutil.move(source_path, destination_path)



source_directory = r"C:\Users\PC\PycharmProjects\lab1\AI\res\TestModel\cars"
#source_directory = r"C:\Users\PC\PycharmProjects\lab1\structure\trained models\test_sort_photos\no_cars"

destination_directory = r"C:\Users\PC\PycharmProjects\lab1\cars_nocars\cars"
#destination_directory = r"C:\Users\PC\PycharmProjects\lab1\cars_nocars\no_cars"
move_files(source_directory, destination_directory)
