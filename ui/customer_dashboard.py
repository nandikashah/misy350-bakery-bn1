import streamlit as st
import time
from services.ai_assistant import BakeryAIAssistant
from ui.state_manager import SessionStateManager
from shared import constants


class CustomerDashboard:

    def __init__(self, manager) -> None:
        self.manager = manager


    def save_all(self):
        self.manager.save_inventory()
        self.manager.save_orders()


    def main(self):
        user = SessionStateManager.get_user()

        st.sidebar.markdown(f"## Welcome {user['full_name']}!")
        st.sidebar.markdown(f"Cart Items: {len(SessionStateManager.get_cart())}")

        if SessionStateManager.is_order_success():
            st.success("Order placed successfully!")
            SessionStateManager.set_order_success(False)

        st.markdown(f"## Welcome, {user['full_name']}!")
        st.markdown("#### This is the Customer Dashboard")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Browse Items",
    "Cart",
    "My Orders",
    "Cancel Order",
    "AI Assistant"
])
        
        with tab1:
            self.browse_items()

        with tab2:
            self.cart_page(user)

        with tab3:
            self.my_orders(user)

        with tab4:
            self.cancel_order(user)

        with tab5:
            self.ai_assistant(user)


    def browse_items(self):
        col_header, col_cart_btn = st.columns([5, 1])

        with col_header:
            st.markdown("### Place your order!")

        with col_cart_btn:
            if st.button("Go to Cart", key="goto_cart_btn"):
                st.info("Click on the Cart tab at the top to view your cart.")

        selected_item = st.selectbox(
            "Items",
            options=self.manager.inventory,
            key="inventory_selector",
            format_func=lambda item: f"{item['name']} — ${item['price']:.2f} ({item['stock']} in stock)"
        )

        if selected_item["stock"] == 0:
            st.warning("This item is currently out of stock.")

        quantity = st.number_input(
            "Enter the Quantity",
            min_value=1,
            step=1,
            value=1
        )

        if st.button(
            "Add to Cart",
            key="add_to_cart_btn",
            type="primary",
            use_container_width=True
        ):

            result = self.manager.add_to_cart(
                SessionStateManager.get_cart(),
                selected_item,
                quantity
            )

            if result == "Success":
                st.success("Added to cart!")
                st.rerun()
            else:
                st.error(result)


    def cart_page(self, user):
        st.subheader("Your Cart")
        cart = SessionStateManager.get_cart()

        if cart == []:
            st.info("Your cart is empty.")
            return

        total_cost = 0

        for idx, item in enumerate(cart):
            item_total = item["price"] * item["quantity"]
            total_cost += item_total

            stock_item = self.manager.find_item_by_id(item["item_id"])
            current_stock = stock_item["stock"] if stock_item else 0

            col_name, col_qty, col_price, col_update, col_remove = st.columns([3, 2, 2, 1, 1])
            col_name.markdown(f"**{item['item_name']}**")
            col_name.write(f"Price: ${item['price']:.2f}")
            col_name.write(f"Available: {current_stock}")

            quantity = col_qty.number_input(
                "Quantity",
                min_value=1,
                step=1,
                value=item["quantity"],
                key=f"cart_qty_{idx}"
            )

            col_price.write(f"Item Total: ${item_total:.2f}")

            if col_update.button("Update", key=f"update_cart_{idx}"):
                if quantity > current_stock:
                    st.error("Not enough stock available to update quantity.")
                else:
                    cart[idx]["quantity"] = quantity
                    st.success("Cart updated.")
                    st.rerun()

            if col_remove.button("Remove", key=f"remove_cart_{idx}"):
                cart.pop(idx)
                st.success("Item removed from cart.")
                st.rerun()

        st.markdown(f"### Total: ${total_cost:.2f}")

        col_checkout, col_clear = st.columns([2, 1])
        if col_clear.button("Clear Cart", key="clear_cart_btn", type="secondary"):
            SessionStateManager.clear_cart()
            st.success("Cart cleared.")
            st.rerun()

        if col_checkout.button(
            "Checkout",
            key="checkout_tab2",
            type="primary",
            use_container_width=True
        ):
            result = self.manager.checkout(
                cart,
                user["email"]
            )

            if result == "Success":
                self.save_all()
                SessionStateManager.clear_cart()
                SessionStateManager.set_order_success(True)
                st.rerun()
            else:
                st.error(result)


    def my_orders(self, user):
        st.subheader("My Orders")
        user_orders = self.manager.find_orders_by_customer(user["email"])

        if user_orders == []:
            st.info("No orders yet.")
        else:
            st.table(user_orders)

        edit_orders = self.manager.find_placed_orders_by_customer(user["email"])

        if edit_orders == []:
            st.info("No placed orders available to edit.")

        else:
            st.markdown("### Edit a Placed Order")
            order_ids = []
            for order in edit_orders:
                order_ids.append(order["id"])

            selected_order_id = st.selectbox("Select Order to Edit", order_ids)

            new_quantity = st.number_input(
                "New Quantity",
                min_value=1,
                step=1
            )

            if st.button(
                "Update Order",
                key="update_order_btn",
                type="primary",
                use_container_width=True
            ):

                result = self.manager.update_order_quantity(
                    selected_order_id,
                    new_quantity
                )

                if result == "Success":
                    self.save_all()
                    st.success("Order updated!")
                    time.sleep(1)

                    st.rerun()
                else:
                    st.error(result)


    def cancel_order(self, user):
        st.subheader("Cancel Order")
        placed_orders = self.manager.find_placed_orders_by_customer(user["email"])

        if placed_orders == []:
            st.info("No orders to cancel.")

        else:
            order_ids = []
            for order in placed_orders:
                order_ids.append(order["id"])

            selected_order_id = st.selectbox(
                "Select Order to Cancel",
                order_ids
            )

            if st.button(
                "Cancel Selected Order",
                key="cancel_order_btn",
                type="primary",
                use_container_width=True
            ):

                result = self.manager.cancel_order(selected_order_id)

                if result == "Success":
                    self.save_all()
                    st.success("Order cancelled.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result)

    def ai_assistant(self, user):
        st.subheader("AI Bakery Assistant")

        assistant = BakeryAIAssistant(self.manager)

        if not SessionStateManager.get_ai_messages():
            SessionStateManager.set_ai_messages([
                {
                    "role": "assistant",
                    "content": "Hi! Ask me about menu items, your orders, or how to use the bakery app."
                }
            ])

        suggested_questions = [
            "How do I place an order?",
            "Can I cancel a placed order?",
            "What items are available right now?"
        ]

        st.markdown("**Suggested questions for the assistant:**")
        col1, col2, col3 = st.columns(3)
        suggestion_cols = [col1, col2, col3]
        user_input = None

        for idx, question in enumerate(suggested_questions):
            if suggestion_cols[idx].button(question, key=f"suggestion_{idx}"):
                user_input = question

        if user_input is None:
            user_input = st.chat_input("Ask the bakery assistant...")

        if st.button("Clear Chat", key="clear_chat_btn", type="secondary"):
            SessionStateManager.set_ai_messages([
                {
                    "role": "assistant",
                    "content": "Hi! Ask me about menu items, your orders, or how to use the bakery app."
                }
            ])
            st.experimental_rerun()

        for message in SessionStateManager.get_ai_messages():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input:
            st.session_state["ai_messages"].append({
                "role": "user",
                "content": user_input
            })

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    ai_response = assistant.get_response(
                        st.session_state["ai_messages"],
                        user["email"]
                    )

                    st.markdown(ai_response)

            st.session_state["ai_messages"].append({
                "role": "assistant",
                "content": ai_response
            })

            logs = assistant.load_logs()
            logs.append({
                "user_email": user["email"],
                "user_message": user_input,
                "ai_response": ai_response
            })
            assistant.save_logs(logs)
