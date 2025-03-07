class ErrorHandler:
    def __init__(self, error_type, errors, uri, **kwargs):
        self.type = error_type
        self.errors = errors
        self.uri = uri
        for key, value in kwargs.items():
            setattr(self, key, value)
