from src.highlighters.highlighter import Highlighter

from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter


class PythonHighlighter(Highlighter):
    def __init__(self):
        pass

    def highlight(self, code: str) -> str:
        formatter = HtmlFormatter()
        styles = f"<style>\n{formatter.get_style_defs('.highlight')}\n</style>"
        code = highlight(code, PythonLexer(), formatter)
        return f"{styles}\n{code}"
