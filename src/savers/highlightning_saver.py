from abc import ABCMeta, abstractmethod

from src.highlighters.highlighter import Highlighter
from src.savers.saver import Saver


class HighlightingSaver(Saver):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()
        self.highlighter: Highlighter = None

    def set_highlighter(self, highlighter: Highlighter):
        self.highlighter = highlighter

    @abstractmethod
    def save(self, code: str):
        pass
