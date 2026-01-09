import shutil
from pathlib import Path
from fastapi import UploadFile


class FileRepository:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def save_pdf(self, file: UploadFile) -> Path:
        destination = self.data_dir / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return destination