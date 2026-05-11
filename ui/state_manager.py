"""
Session State Manager - Centralized management of Streamlit session state.

This module provides a single point of management for all session state variables.
It ensures consistency in how state is initialized, accessed, and reset.

Session state categories:
1. Account State: User login information (read from BakeryManager)
2. UI State: Current page, form inputs, UI flags
3. Cart State: Shopping cart items (ephemeral, cleared on logout)
4. Transient Flags: Temporary messages, success indicators
"""

import streamlit as st
from shared import constants


class SessionStateManager:
    """
    Centralized manager for Streamlit session state.
    
    Ensures all session keys are properly initialized and provides
    consistent access patterns across the app.
    """
    
    @staticmethod
    def initialize():
        """
        Initialize all session state keys with default values.
        Called once at app startup.
        """
        # Account state
        if constants.SESSION_KEY_LOGGED_IN not in st.session_state:
            st.session_state[constants.SESSION_KEY_LOGGED_IN] = False
        
        if constants.SESSION_KEY_USER not in st.session_state:
            st.session_state[constants.SESSION_KEY_USER] = None
        
        if constants.SESSION_KEY_ROLE not in st.session_state:
            st.session_state[constants.SESSION_KEY_ROLE] = None
        
        # Navigation
        if constants.SESSION_KEY_PAGE not in st.session_state:
            st.session_state[constants.SESSION_KEY_PAGE] = constants.PAGE_LOGIN
        
        # Cart and checkout
        if constants.SESSION_KEY_CART not in st.session_state:
            st.session_state[constants.SESSION_KEY_CART] = []
        
        # Transient flags
        if constants.SESSION_KEY_ORDER_SUCCESS not in st.session_state:
            st.session_state[constants.SESSION_KEY_ORDER_SUCCESS] = False
        
        if constants.SESSION_KEY_AI_MESSAGES not in st.session_state:
            st.session_state[constants.SESSION_KEY_AI_MESSAGES] = []
    
    @staticmethod
    def get_logged_in() -> bool:
        """Get login status."""
        return st.session_state.get(constants.SESSION_KEY_LOGGED_IN, False)
    
    @staticmethod
    def set_logged_in(value: bool) -> None:
        """Set login status."""
        st.session_state[constants.SESSION_KEY_LOGGED_IN] = value
    
    @staticmethod
    def get_user() -> dict:
        """Get current user info."""
        return st.session_state.get(constants.SESSION_KEY_USER)
    
    @staticmethod
    def set_user(user: dict) -> None:
        """Set current user info."""
        st.session_state[constants.SESSION_KEY_USER] = user
    
    @staticmethod
    def get_role() -> str:
        """Get user role (Customer or Owner)."""
        return st.session_state.get(constants.SESSION_KEY_ROLE)
    
    @staticmethod
    def set_role(role: str) -> None:
        """Set user role."""
        st.session_state[constants.SESSION_KEY_ROLE] = role
    
    @staticmethod
    def get_page() -> str:
        """Get current page."""
        return st.session_state.get(constants.SESSION_KEY_PAGE, constants.PAGE_LOGIN)
    
    @staticmethod
    def set_page(page: str) -> None:
        """Set current page."""
        st.session_state[constants.SESSION_KEY_PAGE] = page
    
    @staticmethod
    def get_cart() -> list:
        """Get current cart items."""
        return st.session_state.get(constants.SESSION_KEY_CART, [])
    
    @staticmethod
    def set_cart(cart: list) -> None:
        """Set cart items."""
        st.session_state[constants.SESSION_KEY_CART] = cart
    
    @staticmethod
    def clear_cart() -> None:
        """Clear all cart items."""
        st.session_state[constants.SESSION_KEY_CART] = []
    
    @staticmethod
    def is_order_success() -> bool:
        """Get order success flag."""
        return st.session_state.get(constants.SESSION_KEY_ORDER_SUCCESS, False)
    
    @staticmethod
    def set_order_success(value: bool) -> None:
        """Set order success flag."""
        st.session_state[constants.SESSION_KEY_ORDER_SUCCESS] = value
    
    @staticmethod
    def get_ai_messages() -> list:
        """Get AI chat messages."""
        return st.session_state.get(constants.SESSION_KEY_AI_MESSAGES, [])
    
    @staticmethod
    def set_ai_messages(messages: list) -> None:
        """Set AI chat messages."""
        st.session_state[constants.SESSION_KEY_AI_MESSAGES] = messages
    
    @staticmethod
    def add_ai_message(role: str, content: str) -> None:
        """Add a message to AI chat history."""
        messages = st.session_state.get(constants.SESSION_KEY_AI_MESSAGES, [])
        messages.append({"role": role, "content": content})
        st.session_state[constants.SESSION_KEY_AI_MESSAGES] = messages
    
    @staticmethod
    def reset_on_logout() -> None:
        """
        Reset all session state when user logs out.
        Keeps only app-level settings, clears all user-specific state.
        """
        st.session_state[constants.SESSION_KEY_LOGGED_IN] = False
        st.session_state[constants.SESSION_KEY_USER] = None
        st.session_state[constants.SESSION_KEY_ROLE] = None
        st.session_state[constants.SESSION_KEY_PAGE] = constants.PAGE_LOGIN
        st.session_state[constants.SESSION_KEY_CART] = []
        st.session_state[constants.SESSION_KEY_ORDER_SUCCESS] = False
        st.session_state[constants.SESSION_KEY_AI_MESSAGES] = []
