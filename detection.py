import cv2
import numpy as np
from skimage import measure
from scipy import ndimage

def determine_color_category(mean_color):
    # Пример: определение категории цвета на основе среднего цвета
    # Можно дополнительно настроить для определения цвета на основе RGB-значений
    if mean_color[0] > 200 and mean_color[1] < 50 and mean_color[2] < 50:
        return "Red"
    elif mean_color[0] < 50 and mean_color[1] > 200 and mean_color[2] < 50:

        return "Green"
    elif mean_color[0] < 50 and mean_color[1] < 50 and mean_color[2] > 200:
        return "Blue"
    else:
        return "Unknown"

# Функция для обнаружения и анализа частиц микропластика
def analyze_microplastic(image_path):
    # Загрузка изображения
    img = cv2.imread(image_path)

    # Преобразование изображения в оттенки серого
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    #cv2.imshow(gray)
    # Apply thresholding

    # Бинаризация изображения
    _, binary = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    #cv2.imshow(binary)

    # Избавление от шумов
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((1, 1), np.uint8))

    # Нахождение контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создание маски для частиц
    particle_mask = np.zeros_like(gray)

    # Параметры для анализа частиц
    min_particle_area = 50  # Минимальная площадь частицы
    max_particle_area = 5000  # Максимальная площадь частицы

    # Анализ каждого контура
    for contour in contours:
        area = cv2.contourArea(contour)

        if min_particle_area < area < max_particle_area:
            cv2.drawContours(particle_mask, [contour], -1, 255, thickness=cv2.FILLED)

            # Извлечение свойств частицы (размер, центр, геометрическая категория и т.д.)
            moments = cv2.moments(contour)
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])

            # Получение вырезанного изображения частицы
            #!!! если частица на краю изображения - выдаст ошибку
            particle_image = img[cy - 20:cy + 20,
                             cx - 20:cx + 20]  # Пример: вырезать 40x40 область вокруг центра частицы

            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
            # Цвет частицы (определение категории цвета на основе среднего цвета внутри контура)
            mean_color = cv2.mean(img, mask=mask)[:-1][::-1]  # OpenCV возвращает BGRA, переворачиваем в RGB
            color_category = determine_color_category(mean_color)
            # Вывод результатов
            print(f"Color: {color_category}")
            #cv2.imshow(particle_image)
            blank_image = np.zeros((10,10,3), np.uint8)
            blank_image[::] = (mean_color[2], mean_color[1], mean_color[0])
            print(mean_color)
            #cv2.imshow(blank_image)

    return particle_mask

# Пример использования
input_image_path = "micro.png"
particle_mask = analyze_microplastic(input_image_path)

# Сохранение результата
cv2.imwrite("particle_mask.png", particle_mask)
#cv2.imshow(particle_mask)

img = cv2.imread(input_image_path)
src1_mask=cv2.cvtColor(particle_mask,cv2.COLOR_GRAY2BGR)
mask_out=cv2.subtract(img,src1_mask)
mask_out=cv2.subtract(img,mask_out)
#cv2.imshow(mask_out)