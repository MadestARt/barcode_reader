from barcode_reader.file_checker import FileChecker
from barcode_reader.barcode_extractor import BarcodeExtractor
from barcode_reader.barcode_decoder import BarcodeDecoder


def main():
    file_path = input("Введите абсолютный путь до файла штрихкода: ").strip()
    checker = FileChecker(file_path)

    if not checker.exists():
        print(f"Ошибка: Файл по пути '{file_path}' не существует.")
        return

    if not checker.has_allowed_extension():
        print(f"Ошибка: Недопустимое расширение файла '{checker.extension()}'. "
              f"Разрешены: {', '.join(FileChecker.ALLOWED_EXTENSIONS)}")
        return

    barcode_extractor = BarcodeExtractor(file_path)
    data_binary = barcode_extractor.get_barcode_data_bits()

    barcode_decoder = BarcodeDecoder(data_binary)
    data = barcode_decoder.decode()

    print(data)
if __name__ == "__main__":
    main()