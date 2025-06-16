from barcode_reader.filechecker import FileChecker

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

if __name__ == "__main__":
    main()