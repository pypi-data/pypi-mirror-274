from abc import ABCMeta, abstractmethod


class IEnvironment:
    """
    Generic environment functions
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_environment_variables(self, environment_variables):
        """
        Sets the environment variables
        """
        raise NotImplementedError

    @abstractmethod
    def set_configuration_file(self, configuration_file_path):
        """
        Loads the configuration variables from the given file
        """
        raise NotImplementedError

    @abstractmethod
    def check(self):
        """
        Performs the environment checks
        """
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key):
        """
        Retrieves the value of the given key, or None if it does not exist
        """
        raise NotImplementedError
