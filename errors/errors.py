class NotValidNameError(Exception):
    def __init__(self, error_1: bool, error_2: bool):
        self.error_1 = error_1
        self.error_2 = error_2
