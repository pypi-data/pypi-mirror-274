from abc import ABCMeta, abstractmethod


class IOrchestrator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_mapper(self, mapper_manager):
        """
        Sets the mapper
        """
        raise NotImplementedError

    @abstractmethod
    def set_input_manager(self, input_manager):
        """
        Sets the input manager
        """
        raise NotImplementedError

    @abstractmethod
    def set_transformer_manager(self, transformer_manager):
        """
        Sets the transformer manager
        """
        raise NotImplementedError

    @abstractmethod
    def set_output_manager(self, output_manager):
        """
        Sets the output manager
        """
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """
        Executes the operations
        """
        raise NotImplementedError

    @abstractmethod
    def get_summary(self):
        """
        Provides a summary of the processing
        """
        raise NotImplementedError
