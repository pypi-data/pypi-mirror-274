class NoDataToProcessException(Exception):
    """
    Exception raised when there is no data to process
    """

    def __init__(self, message="No data to process"):
        self.message = message
        super().__init__(self.message)

    def get_message(self):
        return self.message
