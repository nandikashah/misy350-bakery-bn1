"""
Reusable UI components for the bakery app.

This module contains shared UI components used across multiple dashboards
to ensure consistency and reduce code duplication.
"""

import streamlit as st
from shared import constants, utils


def render_inventory_selector(inventory):
    """
    Render a selectbox for inventory selection with formatted labels.
    
    Shows item name, price, and stock level.
    
    Args:
        inventory: List of inventory items
        
    Returns:
        Selected inventory item dict, or None if inventory is empty
    """
    if not inventory:
        st.warning("No items available in inventory.")
        return None
    
    selected_item = st.selectbox(
        "Items",
        options=inventory,
        key="inventory_selector",
        format_func=lambda item: utils.format_inventory_label(
            item['name'],
            item['price'],
            item['stock']
        )
    )
    
    return selected_item


def render_stock_warning(item):
    """
    Display a warning if item is out of stock.
    
    Args:
        item: Inventory item dict
    """
    if item and item["stock"] == 0:
        st.warning("This item is currently out of stock.")


def render_low_stock_indicator(item, threshold=constants.INVENTORY_LOW_STOCK_THRESHOLD):
    """
    Display an indicator if item stock is low.
    
    Args:
        item: Inventory item dict
        threshold: Stock level to consider "low"
    """
    if item and 0 < item["stock"] <= threshold:
        st.info(f"⚠️ Low stock: only {item['stock']} left!")


def render_order_table(orders):
    """
    Render orders in a table format.
    
    Args:
        orders: List of order dicts
    """
    if not orders:
        st.info("No orders found.")
        return
    
    st.table(orders)


def render_inventory_table(inventory):
    """
    Render inventory in a table format.
    
    Args:
        inventory: List of inventory item dicts
    """
    if not inventory:
        st.info("No inventory items.")
        return
    
    st.table(inventory)


def render_success_message(message: str) -> None:
    """
    Render a success message.
    
    Args:
        message: Message text to display
    """
    st.success(message)


def render_error_message(message: str) -> None:
    """
    Render an error message.
    
    Args:
        message: Message text to display
    """
    st.error(message)


def render_info_message(message: str) -> None:
    """
    Render an info message.
    
    Args:
        message: Message text to display
    """
    st.info(message)


def render_warning_message(message: str) -> None:
    """
    Render a warning message.
    
    Args:
        message: Message text to display
    """
    st.warning(message)
