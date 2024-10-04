from datetime import datetime
import cv2
import os

"""
Contains functions to extract frames from videos, process all videos in a specified folder,
and save the extracted frames as images. Uses OpenCV for video processing and frame extraction.

Functions:
- video_to_frames(video_path, output_path): Extract frames from a video and save them as images.
- process_all_videos_in_folder(input_folder, output_folder): Process all videos in a folder by
  calling video_to_frames function for each video.

Modules:
- datetime: Used to generate unique names for the extracted frames.
- cv2: OpenCV library for video processing.
- os: Used for file operations and path handling.
"""
def video_to_frames(video_path, output_path):
    # Відкриття відео
    vidcap = cv2.VideoCapture(video_path)

    # Отримання FPS відео
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    if(fps == 0):
        fps = 1

    # Отримання кількості кадрів у відео
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Обчислення загальної тривалості відео в секундах
    total_seconds = frame_count / fps
    print(f"Processing {video_path}: {total_seconds:.2f} seconds")

    if total_seconds < 1:
        print("Video is too short to extract frames.")
        return

    # Визначення часу для зняття кадрів
    if total_seconds <= 3:
        timestamps = [i for i in range(int(total_seconds))]
    else:
        timestamps = [0, total_seconds / 2, total_seconds - 1]

    # Зчитування кадрів і збереження відповідно до часу
    for i, timestamp in enumerate(timestamps):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        success, image = vidcap.read()
        if success:
            base_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(i)
            file_name = f"{base_name}.jpg"
            file_path = os.path.join(output_path, file_name)

            # Перевірка наявності файлу та зміна назви у разі необхідності
            unique_count = 1
            while os.path.exists(file_path):
                file_name = f"{base_name}_{unique_count}.jpg"
                file_path = os.path.join(output_path, file_name)
                unique_count += 1

            cv2.imwrite(file_path, image)
            print(f'Frame {i} extracted successfully from {video_path} as {file_name}')
        else:
            print(f"Failed to extract frame at {timestamp:.2f} seconds from {video_path}")

def process_all_videos_in_folder(input_folder, output_folder):
    # Отримання списку всіх файлів у теці
    video_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Перебір кожного файлу відео
    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)

        # Виклик функції для збереження кадрів
        video_to_frames(video_path, output_folder)

# Вказати шлях до теки з відео
input_folder = r"C:\Users\PC\PycharmProjects\new video&photo\Video for dataset\with_cars"

# Вказати шлях до теки, де зберігатимуться фотографії
output_folder = r"C:\Users\PC\PycharmProjects\new video&photo\photo for dataset\cars"

# Створення теки виводу, якщо вона не існує
os.makedirs(output_folder, exist_ok=True)

# Виклик функції для обробки всіх відео у теці
process_all_videos_in_folder(input_folder, output_folder)
