import os
import xml.etree.ElementTree as ET
from PIL import Image
import numpy as np
import tensorflow as tf

"""
A function that saves an XML file with annotation information.
It takes in parameters like folder, filename, path, width, height, depth, objects, and output_dir to create the XML structure and write it to a file.
"""
# Функція для збереження XML файлу
def save_xml(folder, filename, path, width, height, depth, objects, output_dir):
    annotation = ET.Element('annotation', verified="yes")

    folder_elem = ET.SubElement(annotation, 'folder')
    folder_elem.text = folder

    filename_elem = ET.SubElement(annotation, 'filename')
    filename_elem.text = filename

    path_elem = ET.SubElement(annotation, 'path')
    path_elem.text = path

    source_elem = ET.SubElement(annotation, 'source')
    database_elem = ET.SubElement(source_elem, 'database')
    database_elem.text = "Unknown"

    size_elem = ET.SubElement(annotation, 'size')
    width_elem = ET.SubElement(size_elem, 'width')
    width_elem.text = str(width)
    height_elem = ET.SubElement(size_elem, 'height')
    height_elem.text = str(height)
    depth_elem = ET.SubElement(size_elem, 'depth')
    depth_elem.text = str(depth)

    segmented_elem = ET.SubElement(annotation, 'segmented')
    segmented_elem.text = "0"

    for obj in objects:
        object_elem = ET.SubElement(annotation, 'object')
        name_elem = ET.SubElement(object_elem, 'name')
        name_elem.text = obj['name']

        pose_elem = ET.SubElement(object_elem, 'pose')
        pose_elem.text = "Unspecified"

        truncated_elem = ET.SubElement(object_elem, 'truncated')
        truncated_elem.text = "0"

        difficult_elem = ET.SubElement(object_elem, 'difficult')
        difficult_elem.text = "0"

        bndbox_elem = ET.SubElement(object_elem, 'bndbox')
        xmin_elem = ET.SubElement(bndbox_elem, 'xmin')
        xmin_elem.text = str(int(obj['xmin']))
        ymin_elem = ET.SubElement(bndbox_elem, 'ymin')
        ymin_elem.text = str(int(obj['ymin']))
        xmax_elem = ET.SubElement(bndbox_elem, 'xmax')
        xmax_elem.text = str(int(obj['xmax']))
        ymax_elem = ET.SubElement(bndbox_elem, 'ymax')
        ymax_elem.text = str(int(obj['ymax']))

    tree = ET.ElementTree(annotation)
    xml_output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.xml')
    tree.write(xml_output_path)

# Функція для завантаження зображення і отримання передбачень
def process_images(model, input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(input_dir, filename)
            image = Image.open(file_path)
            width, height = image.size
            depth = len(image.getbands())

            # Передбачення координат за допомогою моделі
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            pred_bbox = model.predict(image_array)[0]

            # Підготовка об'єктів для збереження
            objects = [{
                'name': 'object',  # Замість 'object' потрібно вказати ім'я об'єкта
                'xmin': pred_bbox[0] ,
                'ymin': pred_bbox[1] ,
                'xmax': pred_bbox[2] ,
                'ymax': pred_bbox[3]
            }]

            save_xml(
                folder=os.path.basename(input_dir),
                filename=filename,
                path=file_path,
                width=width,
                height=height,
                depth=depth,
                objects=objects,
                output_dir=output_dir
            )

# Приклад використання:
# from your_model import YourModel  # Імпортуйте вашу модель
# model = YourModel()  # Ініціалізуйте вашу модель
model_path = r"C:\Users\PC\PycharmProjects\AMA_car_object_detection\train_test\saved_model.h5"
input_directory = r"C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\dataset\data\testing_images"
output_directory = r"C:\Users\PC\PycharmProjects\AMA_many_car_object_detection\dataset\data\testing_images"

model = tf.keras.models.load_model(model_path)

process_images(model, input_directory, output_directory)
