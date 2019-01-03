from src.savers.highlightning_saver import HighlightingSaver


class HtmlSaver(HighlightingSaver):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.filename = filename

    def save(self, code: str):
        code = f"<html>\n{self.highlighter.highlight(code)}</html>"
        with open(self.filename, 'w') as file:
            file.writelines(code)
