import os

"""
A function that deletes all files in the specified directory.
Parameters:
directory_path (str): The path to the directory containing the files to be deleted.
Returns:
None
"""

def delete_files_in_directory(directory_path):
    # Отримуємо список файлів у директорії
    files = os.listdir(directory_path)

    # Видаляємо кожен файл у цьому списку
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        try:
            os.remove(file_path)
            print(f"Файл {file_name} був успішно видалений")
        except Exception as e:
            print(f"Помилка при видаленні файлу {file_name}: {e}")


directory_path = r'photos/no_cars'
delete_files_in_directory(directory_path)

