class NotValidNameError(Exception):
    def __init__(self, error1: bool = False, error2: bool = False):
        self.error1 = error1
        self.error2 = error2
