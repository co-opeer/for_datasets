import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import os

# Завантаження CSV файлу
csv_path = r'C:\Users\PC\PycharmProjects\for_datasets\json3d\processed_annotations.csv'  # Вкажіть шлях до вашого CSV файлу
data = pd.read_csv(csv_path)
previous_image = None
img = None
counter=0
# Завантаження зображення
image_path = r"C:\Users\PC\PycharmProjects\for_datasets\json3d\norm_img"  # Вкажіть шлях до вашої папки із зображеннями
for index, row in data.iterrows():
    counter+=1
    print(counter)
   # if counter <19: continue

    image_path = os.path.join(image_path, row['image'])

    if previous_image != row['image']:
        previous_image = row['image']
        img = Image.open(image_path)


    fig, ax = plt.subplots(1)
    ax.imshow(img)

    x_center = row['xcenter']
    y_center = row['ycenter']

    # Додавання ліній від центру в напрямку ширини, висоти та довжини
    line_xwidth = lines.Line2D([x_center,  row['xwidth']], [y_center, row['ywidth']], color='r')
    ax.add_line(line_xwidth)

    line_ywidth = lines.Line2D([x_center,  row['xheight']], [y_center, row['yheight']], color='g')
    ax.add_line(line_ywidth)

    line_xheight = lines.Line2D([x_center,  row['xlength']], [y_center, row['ylength']], color='b')
    ax.add_line(line_xheight)
    plt.show()


