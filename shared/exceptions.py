"""
Custom exceptions for the bakery app.
Centralized exception hierarchy for error handling across all layers.
"""


class BakeryAppException(Exception):
    """Base exception for all bakery app errors."""
    def __init__(self, message: str, error_type: str = "error"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)


class ValidationError(BakeryAppException):
    """Raised when input validation fails."""
    def __init__(self, message: str):
        super().__init__(message, "validation_error")


class NotFoundError(BakeryAppException):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str):
        super().__init__(message, "not_found")


class InsufficientStockError(BakeryAppException):
    """Raised when there is insufficient stock for an operation."""
    def __init__(self, message: str):
        super().__init__(message, "insufficient_stock")


class DuplicateEmailError(BakeryAppException):
    """Raised when trying to register with an already-used email."""
    def __init__(self, message: str):
        super().__init__(message, "duplicate_email")


class UnauthorizedError(BakeryAppException):
    """Raised when user lacks permission for an operation."""
    def __init__(self, message: str):
        super().__init__(message, "unauthorized")
