"""
Type definitions and data transfer objects (DTOs) for the bakery app.
Provides structured types for data passing between layers.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class UserDTO:
    """Data transfer object for User."""
    id: str
    full_name: str
    email: str
    role: str


@dataclass
class InventoryItemDTO:
    """Data transfer object for InventoryItem."""
    item_id: str
    name: str
    price: float
    stock: int


@dataclass
class CartItemDTO:
    """Data transfer object for CartItem."""
    item_id: str
    item_name: str
    price: float
    quantity: int


@dataclass
class OrderDTO:
    """Data transfer object for Order."""
    id: str
    customer_email: str
    item_id: str
    item_name: str
    quantity: int
    status: str
    total: float


@dataclass
class CommandResponse:
    """Response wrapper for command operations (write operations)."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error_type": self.error_type,
        }


@dataclass
class QueryResponse:
    """Response wrapper for query operations (read operations)."""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message,
        }
