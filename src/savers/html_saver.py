from src.savers.highlightning_saver import HighlightingSaver


class HtmlSaver(HighlightingSaver):
    def __init__(self):
        super().__init__()

    def save(self, code: str):
        pass
