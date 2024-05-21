from abc import ABCMeta, abstractmethod


class ITransformerManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_id(self):
        """
        Retrieves the manager ID
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, *args):
        """
        Transforms the input data
        """
        raise NotImplementedError
