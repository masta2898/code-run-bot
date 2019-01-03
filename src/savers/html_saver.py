from src.savers.highlightning_saver import HighlightingSaver


class HtmlSaver(HighlightingSaver):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.filename = filename

    def save(self, code: str) -> str:
        if self._highlighter:
            code = f"<html>\n{self._highlighter.highlight(code)}</html>"
        with open(self.filename, 'w') as file:
            file.writelines(code)
        return f"Saved in html as {self.filename}"
