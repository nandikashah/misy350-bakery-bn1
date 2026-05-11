"""
Utility functions for validation and formatting.
Centralized helpers used across all layers.
"""

import re
from typing import Optional
from shared.exceptions import ValidationError


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def validate_required_field(value: Optional[str], field_name: str) -> None:
    """
    Validate that a required field is not empty.
    
    Args:
        value: Value to validate
        field_name: Name of field for error message
        
    Raises:
        ValidationError if field is empty
    """
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{field_name} is required.")


def validate_quantity(quantity: int, min_value: int = 1) -> None:
    """
    Validate quantity is a positive integer.
    
    Args:
        quantity: Quantity to validate
        min_value: Minimum allowed value (default 1)
        
    Raises:
        ValidationError if quantity is invalid
    """
    try:
        qty = int(quantity)
        if qty < min_value:
            raise ValidationError(f"Quantity must be at least {min_value}.")
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a valid number.")


def validate_price(price: float) -> None:
    """
    Validate price is a positive number.
    
    Args:
        price: Price to validate
        
    Raises:
        ValidationError if price is invalid
    """
    try:
        p = float(price)
        if p < 0:
            raise ValidationError("Price must be a positive number.")
    except (ValueError, TypeError):
        raise ValidationError("Price must be a valid number.")


def format_price(price: float) -> str:
    """
    Format price for display.
    
    Args:
        price: Price to format
        
    Returns:
        Formatted price string (e.g., "$12.99")
    """
    return f"${price:.2f}"


def format_inventory_label(name: str, price: float, stock: int) -> str:
    """
    Format inventory item label for selectbox display.
    
    Args:
        name: Item name
        price: Item price
        stock: Stock quantity
        
    Returns:
        Formatted label
    """
    return f"{name} — {format_price(price)} ({stock} in stock)"
