from abc import ABCMeta, abstractmethod

from src.highlighters.highlighter import Highlighter
from src.savers.saver import Saver


class HighlightingSaver(Saver):
    __metaclass__ = ABCMeta

    def __init__(self, filename: str):
        super().__init__(filename)
        self.filename = filename
        self._highlighter: Highlighter = None

    def set_highlighter(self, highlighter: Highlighter):
        self._highlighter = highlighter

    @abstractmethod
    def save(self, code: str):
        raise NotImplementedError
