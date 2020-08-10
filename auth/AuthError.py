# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code = 401):
        self.error = error
        self.status_code = status_code