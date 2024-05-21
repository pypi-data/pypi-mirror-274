class AbortProcessException(Exception):
    """
    Exception that aborts the process
    """

    def __init__(self, code, message=""):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def set_code(self, code):
        self.code = code

    def set_message(self, message):
        self.message = message
        super().message = message

    def get_message(self):
        return self.code

    def get_code(self):
        return self.code
