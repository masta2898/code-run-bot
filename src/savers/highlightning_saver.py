from abc import ABCMeta, abstractmethod

from src.highlighters.highlighter import Highlighter
from src.savers.saver import Saver


class HighlightingSaver(Saver):
    __metaclass__ = ABCMeta

    def __init__(self, filename: str):
        super().__init__(filename)
        self.filename = filename
        self.highlighter: Highlighter = None

    def set_highlighter(self, highlighter: Highlighter):
        self.highlighter = highlighter

    def get_highlighter(self):
        return self.highlighter

    @abstractmethod
    def save(self, code: str):
        raise NotImplementedError
