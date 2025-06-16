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

        # Определяем среднюю ширину одного бита, отловив стартовую последовательность
        start, end = -1, -1
        curren_bits = ""
        for p in range(extended_width - 2):
            if hor_data[p] < avg and hor_data[p + 1] > avg:
                curren_bits += "1"
                if start == -1:
                    start = p
                if curren_bits == "101":
                    end = p
                    break
            if hor_data[p] > avg and hor_data[p + 1] < avg:
                curren_bits += "0"

        bit_width = int((end - start) / 3)

        # Записываем результат, определяя число бит в каждом интервале между переходами через середину
        # (Опираясь на ширину одного бита)
        result_bits = ""
        for l in range(extended_width - 2):
            if hor_data[l] > avg and hor_data[l + 1] < avg:
                interval = l - start
                cnt = interval / bit_width
                result_bits += "1" * int(round(cnt))
                start = l
            if hor_data[l] < avg and hor_data[l + 1] > avg:
                interval = l - start
                cnt = interval / bit_width
                result_bits += "0" * int(round(cnt))
                start = l

        return result_bits