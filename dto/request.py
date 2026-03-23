class Request:
    def __init__(self, path: str, method: str, query_params: dict, form_data: dict):
        self.path = path
        self.method = method
        self.query_params = query_params
        self.form_data = form_data
