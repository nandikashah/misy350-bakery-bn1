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

# Order status transition rules - which statuses can transition to which
ORDER_STATUS_TRANSITIONS = {
    ORDER_STATUS_PLACED: [ORDER_STATUS_COMPLETED, ORDER_STATUS_SHIPPED, ORDER_STATUS_CANCELLED],
    ORDER_STATUS_COMPLETED: [],  # Terminal state
    ORDER_STATUS_SHIPPED: [],    # Terminal state
    ORDER_STATUS_CANCELLED: [],  # Terminal state
}

ORDER_STATUS_FINAL = [
    ORDER_STATUS_COMPLETED,
    ORDER_STATUS_SHIPPED,
    ORDER_STATUS_CANCELLED,
]

# Order ID generation
ORDER_ID_PREFIX = "#"
ORDER_ID_START = 1000

# User role constants
USER_ROLE_CUSTOMER = "Customer"
USER_ROLE_OWNER = "Owner"

USER_ROLES = [USER_ROLE_CUSTOMER, USER_ROLE_OWNER]

# Inventory constants
INVENTORY_LOW_STOCK_THRESHOLD = 5

# Validation constants
EMAIL_MIN_LENGTH = 5
EMAIL_MAX_LENGTH = 254
PASSWORD_MIN_LENGTH = 8
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 100

# Session state keys
SESSION_KEY_LOGGED_IN = "logged_in"
SESSION_KEY_USER = "user"
SESSION_KEY_ROLE = "role"
SESSION_KEY_PAGE = "page"
SESSION_KEY_CART = "cart"
SESSION_KEY_ORDER_SUCCESS = "order_success"
SESSION_KEY_AI_MESSAGES = "ai_messages"
SESSION_KEY_ACTIVE_CUSTOMER_TAB = "active_customer_tab"
SESSION_KEY_CART_REVIEW = "cart_review"

# Page names
PAGE_LOGIN = "login"
PAGE_CUSTOMER = "customer"
PAGE_OWNER = "owner"

# Customer tab constants
CUSTOMER_TAB_BROWSE = "browse"
CUSTOMER_TAB_CART = "cart"
CUSTOMER_TAB_MY_ORDERS = "my_orders"
CUSTOMER_TAB_CANCEL_ORDER = "cancel_order"
CUSTOMER_TAB_AI_ASSISTANT = "ai_assistant"
