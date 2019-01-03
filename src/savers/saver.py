from abc import ABCMeta, abstractmethod


class Saver:
    __metaclass__ = ABCMeta

    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def save(self, code: str):
        raise NotImplementedError
