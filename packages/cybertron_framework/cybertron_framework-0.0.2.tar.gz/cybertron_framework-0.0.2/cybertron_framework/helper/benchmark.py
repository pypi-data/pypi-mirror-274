import time


class Benchmark:
    """
    Performs benchmark of the app's execution
    """

    def __init__(self):
        self.timestamp = {}

    def start(self, benchmark_key):
        self.timestamp[benchmark_key] = time.time()

    def end(self, benchmark_key):
        return str(round(time.time() - self.timestamp[benchmark_key], 2))
