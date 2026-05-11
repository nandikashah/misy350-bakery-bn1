"""
Enums for the bakery app.
Provides type-safe alternatives to magic strings.
"""

from enum import Enum


class OrderStatus(Enum):
    """Order status enumeration."""
    PLACED = "Placed"
    COMPLETED = "Completed"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"


class UserRole(Enum):
    """User role enumeration."""
    CUSTOMER = "Customer"
    OWNER = "Owner"


class ErrorType(Enum):
    """Error type enumeration for validation and business logic."""
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    INSUFFICIENT_STOCK = "insufficient_stock"
    DUPLICATE_EMAIL = "duplicate_email"
    UNAUTHORIZED = "unauthorized"
    INTERNAL_ERROR = "internal_error"
