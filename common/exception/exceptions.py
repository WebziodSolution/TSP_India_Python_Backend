class GlobalException(Exception):
    """
    Custom exception representing general validation/operational issues,
    matching GlobalException.java.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
