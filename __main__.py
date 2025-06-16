from barcode_reader.file_checker import FileChecker
from barcode_reader.barcode_extractor import BarcodeExtractor

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

    data = barcode_extractor.get_barcode_data_bits()

    print(data)

if __name__ == "__main__":
    main()