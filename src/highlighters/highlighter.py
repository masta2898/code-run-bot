from abc import ABCMeta, abstractmethod


class Highlighter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def highlight(self, code: str) -> str:
        raise NotImplementedError
