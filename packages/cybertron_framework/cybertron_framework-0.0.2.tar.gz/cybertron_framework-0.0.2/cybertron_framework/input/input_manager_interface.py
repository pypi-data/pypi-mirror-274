from abc import ABCMeta, abstractmethod


class IInputManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_id(self):
        """
        Retrieves the manager ID
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self):
        """
        Retrieves the input data
        """
        raise NotImplementedError
