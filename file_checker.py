import os

class FileChecker:
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

    def __init__(self, file_path):
        self.file_path = file_path

    def exists(self):
        return os.path.isfile(self.file_path)

    def extension(self):
        _, ext = os.path.splitext(self.file_path)
        return ext.lower()

    def has_allowed_extension(self):
        return self.extension() in self.ALLOWED_EXTENSIONS
