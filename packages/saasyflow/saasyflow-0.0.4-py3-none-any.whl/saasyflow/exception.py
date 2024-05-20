class SaasyflowException(Exception):
    def __init__(self, message, status_code, errors, is_general) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.errors = errors
        self.is_genral = is_general
