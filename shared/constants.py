"""
Centralized constants for the bakery app.
Used across services, UI, and data layers to avoid magic strings.
"""

# Order status constants
ORDER_STATUS_PLACED = "Placed"
ORDER_STATUS_COMPLETED = "Completed"
ORDER_STATUS_SHIPPED = "Shipped"
ORDER_STATUS_CANCELLED = "Cancelled"

ORDER_STATUSES = [
    ORDER_STATUS_PLACED,
    ORDER_STATUS_COMPLETED,
    ORDER_STATUS_SHIPPED,
    ORDER_STATUS_CANCELLED,
]

# User role constants
USER_ROLE_CUSTOMER = "Customer"
USER_ROLE_OWNER = "Owner"

USER_ROLES = [USER_ROLE_CUSTOMER, USER_ROLE_OWNER]

# Inventory constants
INVENTORY_LOW_STOCK_THRESHOLD = 5

# Session state keys
SESSION_KEY_LOGGED_IN = "logged_in"
SESSION_KEY_USER = "user"
SESSION_KEY_ROLE = "role"
SESSION_KEY_PAGE = "page"
SESSION_KEY_CART = "cart"
SESSION_KEY_ORDER_SUCCESS = "order_success"
SESSION_KEY_AI_MESSAGES = "ai_messages"

# Page names
PAGE_LOGIN = "login"
PAGE_CUSTOMER = "customer"
PAGE_OWNER = "owner"
