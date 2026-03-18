class Validator:
    def is_name_valid(self, name):
        return 0 < len(name) < 36 if name else False
