class SentrifyAIError(Exception):
    """Base class for exceptions in this module."""
    pass

class ModelNotFoundError(SentrifyAIError):
    """Exception raised when the requested model is not found."""
    pass

class APIRequestError(SentrifyAIError):
    """Exception raised for errors in the API request."""
    pass
