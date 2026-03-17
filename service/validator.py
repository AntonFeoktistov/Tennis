class Validator:
    def validate_name(self, name):
        return 0 < name < 36 if name else False
