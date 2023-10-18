import os
import cv2
import shutil
from sklearn.cluster import KMeans
from collections import Counter


def get_dominant_color(image, k=4):
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(image)

    label_counts = Counter(labels)

    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return list(dominant_color)


def sort(input_folder, output_folder):
    files = os.listdir(input_folder)

    image_colors = []

    for file in files:
        bgr_image = cv2.imread(f'{input_folder}/{file}')
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        dom_color = get_dominant_color(hsv_image)
        image_colors.append([file, dom_color])

    image_colors.sort(key=lambda x: x[1])

    for i, (file, _) in enumerate(image_colors):
        new_file_name = f'{i+1}.jpg'
        shutil.move(f'{input_folder}/{file}',
                    f'{output_folder}/{new_file_name}')
