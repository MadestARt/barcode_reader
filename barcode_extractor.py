import cv2
import numpy as np

class BarcodeExtractor:

    def __init__(self, valid_image_path):
        self.valid_image_path = valid_image_path

    def get_barcode_data_bits(self):
        # Загружаем изображение
        img = cv2.imread(self.valid_image_path)

        # Получаем размеры изображения
        height, width = img.shape[:2]

        # Изменение ширины (увеличение в 4 раза), сохраняя высоту
        extended_width = width * 4
        img_resized = cv2.resize(img, (extended_width, height), interpolation=cv2.INTER_AREA)

        # Извлекаем горизонтальную линию посередине изображения высотой 1 пиксель
        middle_height = height // 2
        hor_line = img_resized[middle_height:middle_height + 1, :, :]

        # Перевод в градации серого
        hor_line_gray = cv2.cvtColor(hor_line, cv2.COLOR_BGR2GRAY)

        # Преобразование в одномерный массив NumPy
        hor_data = hor_line_gray[0].astype(np.int32)

        # В изображении в оттенках серого черный = 0, а белый = 255.
        # Для бинаризации штрихкода часто используют черное = 1, белое = 0, поэтому необходимо инвертировать
        hor_data = 255 - hor_data
        avg = np.average(hor_data)

        pos1, pos2 = -1, -1
        bits = ""
        for p in range(extended_width - 2):
            if hor_data[p] < avg and hor_data[p + 1] > avg:
                bits += "1"
                if pos1 == -1:
                    pos1 = p
                if bits == "101":
                    pos2 = p
                    break
            if hor_data[p] > avg and hor_data[p + 1] < avg:
                bits += "0"

        bit_width = int((pos2 - pos1) / 3)
        print(bit_width)

        result_bits = ""
        for l in range(extended_width - 2):
            if hor_data[l] > avg and hor_data[l + 1] < avg:
                interval = l - pos1
                cnt = interval / bit_width
                result_bits += "1" * int(round(cnt))
                pos1 = l
            if hor_data[l] < avg and hor_data[l + 1] > avg:
                interval = l - pos1
                cnt = interval / bit_width
                result_bits += "0" * int(round(cnt))
                pos1 = l

        return result_bits