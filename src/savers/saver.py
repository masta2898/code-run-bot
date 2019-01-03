from abc import ABCMeta, abstractmethod


class Saver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, code: str):
        raise NotImplementedError
