"""
Utility functions for validation and formatting.
Centralized helpers used across all layers.
"""

import re
from typing import Optional, List, Dict, Any
from shared.exceptions import ValidationError
from shared import constants


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

    email = email.strip()
    if len(email) < constants.EMAIL_MIN_LENGTH or len(email) > constants.EMAIL_MAX_LENGTH:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> None:
    """
    Validate password strength.

    Args:
        password: Password to validate

    Raises:
        ValidationError if password is invalid
    """
    if not password or len(password) < constants.PASSWORD_MIN_LENGTH:
        raise ValidationError(f"Password must be at least {constants.PASSWORD_MIN_LENGTH} characters long.")


def validate_name(name: str) -> None:
    """
    Validate name field.

    Args:
        name: Name to validate

    Raises:
        ValidationError if name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValidationError("Name is required.")

    name = name.strip()
    if len(name) < constants.NAME_MIN_LENGTH or len(name) > constants.NAME_MAX_LENGTH:
        raise ValidationError(f"Name must be between {constants.NAME_MIN_LENGTH} and {constants.NAME_MAX_LENGTH} characters.")


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


def validate_order_status_transition(current_status: str, new_status: str) -> None:
    """
    Validate that an order status transition is allowed.

    Args:
        current_status: Current order status
        new_status: Proposed new status

    Raises:
        ValidationError if transition is not allowed
    """
    if current_status not in constants.ORDER_STATUSES:
        raise ValidationError(f"Invalid current status: {current_status}")

    if new_status not in constants.ORDER_STATUSES:
        raise ValidationError(f"Invalid new status: {new_status}")

    allowed_transitions = constants.ORDER_STATUS_TRANSITIONS.get(current_status, [])
    if new_status not in allowed_transitions:
        raise ValidationError(f"Cannot change order status from '{current_status}' to '{new_status}'.")


def generate_order_number(existing_orders: List[Dict[str, Any]]) -> str:
    """
    Generate a new readable order number for a transaction.

    Args:
        existing_orders: List of existing orders to determine next order number

    Returns:
        New order number in format #1001, #1002, etc.
    """
    existing_nums = []
    for order in existing_orders:
        order_number = order.get("order_number", "")
        if isinstance(order_number, str) and order_number.startswith(constants.ORDER_ID_PREFIX):
            try:
                num = int(order_number[1:])
                existing_nums.append(num)
            except ValueError:
                continue

    next_num = constants.ORDER_ID_START
    if existing_nums:
        next_num = max(existing_nums) + 1

    return f"{constants.ORDER_ID_PREFIX}{next_num}"


def get_order_label(order: Dict[str, Any]) -> str:
    """
    Get a display label for an order.

    Args:
        order: Order dictionary

    Returns:
        Readable order label using order number or internal id fallback.
    """
    order_number = order.get("order_number")
    if order_number:
        return order_number

    internal_id = order.get("id", "")
    if isinstance(internal_id, str) and len(internal_id) > 8:
        return f"{internal_id[:8]}..."

    return str(internal_id)


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


def calculate_cart_total(cart: List[Dict[str, Any]]) -> float:
    """
    Calculate total price of items in cart.

    Args:
        cart: List of cart items with 'price' and 'quantity' keys

    Returns:
        Total price as float
    """
    total = 0.0
    for item in cart:
        total += item.get("price", 0) * item.get("quantity", 0)
    return round(total, 2)


def prepare_order_data(cart_item: Dict[str, Any], customer_email: str, order_number: str, transaction_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Prepare order data structure for a cart item.
    Supports future multi-item order transactions.

    Args:
        cart_item: Cart item dict with item_id, item_name, price, quantity
        customer_email: Customer's email
        order_number: Readable order number for the transaction
        transaction_id: Optional transaction ID for grouping multi-item orders

    Returns:
        Order data dict ready for storage
    """
    total = round(cart_item["price"] * cart_item["quantity"], 2)

    order_data = {
        "id": "",
        "order_number": order_number,
        "customer_email": customer_email,
        "item_id": cart_item["item_id"],
        "item_name": cart_item["item_name"],
        "quantity": cart_item["quantity"],
        "status": constants.ORDER_STATUS_PLACED,
        "total": total,
    }

    # Add transaction_id for future multi-item order support
    if transaction_id:
        order_data["transaction_id"] = transaction_id

    return order_data
