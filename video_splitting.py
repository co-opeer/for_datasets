from datetime import datetime

import cv2
import os


def video_to_frames(video_path, output_path, desired_fps):
    # Відкриття відео
    vidcap = cv2.VideoCapture(video_path)

    # Отримання FPS відео
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    # Отримання кількості кадрів у відео
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Обчислення загальної тривалості відео в секундах
    total_seconds = frame_count / fps
    print(f"Processing {video_path}: {total_seconds:.2f} seconds")

    # Інтервал між кадрами, які потрібно зберегти
    interval = int(round(fps / desired_fps))

    success, image = vidcap.read()
    count = 0
    frame_num = 0

    # Зчитування кадрів та збереження з інтервалом
    while success:
        if frame_num % interval == 0:
            base_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(count)
            file_name = f"{base_name}.jpg"
            file_path = os.path.join(output_path, file_name)

            # Перевірка наявності файлу та зміна назви у разі необхідності
            unique_count = 1
            while os.path.exists(file_path):
                file_name = f"{base_name}_{unique_count}.jpg"
                file_path = os.path.join(output_path, file_name)
                unique_count += 1

            cv2.imwrite(file_path, image)
            print(f'Frame {count} extracted successfully from {video_path} as {file_name}')
            count += 1
        success, image = vidcap.read()
        frame_num += 1


def process_all_videos_in_folder(input_folder, output_folder, desired_fps):
    # Отримання списку всіх файлів у теці
    video_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Перебір кожного файлу відео
    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)

        # Виклик функції для збереження кадрів
        video_to_frames(video_path, output_folder, desired_fps)


# Вказати шлях до теки з відео
input_folder = r"video/without_cars"

# Вказати шлях до теки, де зберігатимуться фотографії
output_folder = r"photos/no_cars"

# Бажана частота кадрів на секунду (fps)
desired_fps = 1  # Наприклад, 1 кадр на секунду

# Створення теки виводу, якщо вона не існує
os.makedirs(output_folder, exist_ok=True)

# Виклик функції для обробки всіх відео у теці
process_all_videos_in_folder(input_folder, output_folder, desired_fps)
