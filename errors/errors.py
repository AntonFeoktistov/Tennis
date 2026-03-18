class NotValidNameError(Exception):
    def __init__(self, error1: bool, error2: bool):
        self.error1 = error1
        self.error2 = error2
