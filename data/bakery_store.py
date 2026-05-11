"""
BakeryStore - Low-level data persistence layer for JSON files.

This class handles all file I/O operations for the bakery app.
It provides methods to load and save inventory, orders, and users data.

The store maintains JSON files as the source of truth. All changes made in-memory
must be explicitly persisted by calling save methods.

Future improvements:
- Add error handling and retry logic for file operations
- Add transactional safety (write to temp file, then atomic rename)
- Add backup/versioning support
- Add migration support for schema changes
"""

import json
from pathlib import Path


class BakeryStore:
    """
    File-based data store using JSON.
    
    Manages persistence for:
    - inventory.json: Product catalog
    - orders.json: All customer orders
    - users.json: Customer and owner accounts
    """
    
    def __init__(self, data_folder: Path):
        """
        Initialize store with data folder path.
        
        Args:
            data_folder: Path to folder containing JSON files
        """
        self.inventory_path = data_folder / "inventory.json"
        self.orders_path = data_folder / "orders.json"
        self.users_path = data_folder / "users.json"

    # ========== INVENTORY METHODS ==========

    def load_inventory(self):
        """
        Load inventory from inventory.json.
        
        Returns:
            List of inventory items, empty list if file doesn't exist
        """
        if self.inventory_path.exists():
            with open(self.inventory_path, "r") as f:
                return json.load(f)
        return []
    
    def save_inventory(self, inventory):
        """
        Save inventory to inventory.json.
        
        Args:
            inventory: List of inventory items to persist
        """
        with open(self.inventory_path, "w") as f:
            json.dump(inventory, f, indent=4)

    # ========== ORDERS METHODS ==========

    def load_orders(self):
        """
        Load orders from orders.json.
        
        Returns:
            List of orders, empty list if file doesn't exist
        """
        if self.orders_path.exists():
            with open(self.orders_path, "r") as f:
                return json.load(f)
        return []
    
    def save_orders(self, orders):
        """
        Save orders to orders.json.
        
        Args:
            orders: List of orders to persist
        """
        with open(self.orders_path, "w") as f:
            json.dump(orders, f, indent=4)

    # ========== USERS METHODS ==========

    def load_users(self):
        """
        Load users from users.json.
        
        Returns:
            List of users, empty list if file doesn't exist
        """
        if self.users_path.exists():
            with open(self.users_path, "r") as f:
                return json.load(f)
        return []
    
    def save_users(self, users):
        """
        Save users to users.json.
        
        Args:
            users: List of users to persist
        """
        with open(self.users_path, "w") as f:
            json.dump(users, f, indent=4)
