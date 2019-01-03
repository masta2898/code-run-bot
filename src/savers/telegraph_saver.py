from telegraph import Telegraph

from src.savers.highlightning_saver import HighlightingSaver


class TelegraphSaver(HighlightingSaver):
    def __init__(self, title):
        super().__init__(title)
        self.title = title

        self.telegraph = Telegraph()
        self.telegraph.create_account('telegraph_saver')

    def save(self, code: str) -> str:
        if self._highlighter:
            code = self._highlighter.highlight(code)

        response = self.telegraph.create_page(self.title, html_content=code)
        return f"https://telegra.ph/{response['path']}"