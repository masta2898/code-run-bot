from src.savers.saver import Saver


class PlaintextSaver(Saver):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.filename = filename

    def save(self, code: str) -> str:
        with open(self.filename, 'w') as file:
            file.writelines(code)
        return f"Saved to {self.filename}."
