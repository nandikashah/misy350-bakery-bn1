import streamlit as st
import time
from services.ai_assistant import BakeryAIAssistant
from ui.state_manager import SessionStateManager
from shared import constants
from shared.utils import format_inventory_label, format_price, calculate_cart_total, get_order_label


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

        active_tab = SessionStateManager.get_active_customer_tab()
        if active_tab == constants.CUSTOMER_TAB_CART:
            st.markdown("### Cart")
            self.cart_page(user)
            if st.button("Return to Browse", key="return_to_browse"):
                SessionStateManager.set_active_customer_tab(constants.CUSTOMER_TAB_BROWSE)
                SessionStateManager.set_cart_review(False)
                st.rerun()
            return

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
                SessionStateManager.set_active_customer_tab(constants.CUSTOMER_TAB_CART)
                SessionStateManager.set_cart_review(False)
                st.rerun()

        selected_item = st.selectbox(
            "Items",
            options=self.manager.inventory,
            key="inventory_selector",
            format_func=lambda item: format_inventory_label(item['name'], item['price'], item['stock'])
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

        total_cost = calculate_cart_total(cart)

        for idx, item in enumerate(cart):
            item_total = item["price"] * item["quantity"]

            stock_item = self.manager.find_item_by_id(item["item_id"])
            current_stock = stock_item["stock"] if stock_item else 0

            col_name, col_qty, col_price, col_update, col_remove = st.columns([3, 2, 2, 1, 1])
            col_name.markdown(f"**{item['item_name']}**")
            col_name.write(f"Price: {format_price(item['price'])}")
            col_name.write(f"Available: {current_stock}")

            quantity = col_qty.number_input(
                "Quantity",
                min_value=1,
                step=1,
                value=item["quantity"],
                key=f"cart_qty_{idx}"
            )

            col_price.write(f"Item Total: {format_price(item_total)}")

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

        st.markdown(f"### Total: {format_price(total_cost)}")

        if SessionStateManager.is_cart_review():
            st.markdown("#### Review your order before placing it")
            for item in cart:
                item_total = item["price"] * item["quantity"]
                st.write(f"- {item['item_name']} x {item['quantity']} @ {format_price(item['price'])} = {format_price(item_total)}")

            st.markdown(f"**Order Total:** {format_price(total_cost)}")
            col_place, col_edit = st.columns([2, 1])
            if col_edit.button("Edit Cart", key="edit_cart_btn", type="secondary"):
                SessionStateManager.set_cart_review(False)
                st.rerun()
            if col_place.button("Place Order", key="place_order_btn", type="primary", use_container_width=True):
                result = self.manager.checkout(
                    cart,
                    user["email"]
                )

                if result == "Success":
                    self.save_all()
                    SessionStateManager.clear_cart()
                    SessionStateManager.set_cart_review(False)
                    SessionStateManager.set_order_success(True)
                    st.rerun()
                else:
                    st.error(result)
        else:
            col_review, col_clear = st.columns([2, 1])
            if col_clear.button("Clear Cart", key="clear_cart_btn", type="secondary"):
                SessionStateManager.clear_cart()
                SessionStateManager.set_cart_review(False)
                st.success("Cart cleared.")
                st.rerun()

            if col_review.button(
                "Review Order",
                key="review_order_btn",
                type="primary",
                use_container_width=True
            ):
                SessionStateManager.set_cart_review(True)
                st.rerun()


    def my_orders(self, user):
        st.subheader("My Orders")
        user_orders = self.manager.find_orders_by_customer(user["email"])

        if user_orders == []:
            st.info("No orders yet.")
        else:
            self.render_order_cards(user_orders)

        edit_orders = self.manager.find_placed_orders_by_customer(user["email"])

        if edit_orders == []:
            st.info("No placed orders available to edit.")
        else:
            st.markdown("### Edit a Placed Order")
            selected_order = st.selectbox(
                "Select Order to Edit",
                options=edit_orders,
                format_func=lambda order: f"{get_order_label(order)} — {order['item_name']} x {order['quantity']}"
            )

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
                    selected_order["id"],
                    new_quantity
                )

                if result == "Success":
                    self.save_all()
                    st.success("Order updated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result)


    def render_order_cards(self, orders):
        grouped_orders = {}
        for order in orders:
            key = order.get("order_number") or order.get("id")
            grouped_orders.setdefault(key, []).append(order)

        for order_label, order_lines in grouped_orders.items():
            line_statuses = [line.get("status", "Unknown") for line in order_lines]
            unique_statuses = [
                status for status in [
                    constants.ORDER_STATUS_PLACED,
                    constants.ORDER_STATUS_SHIPPED,
                    constants.ORDER_STATUS_COMPLETED,
                    constants.ORDER_STATUS_CANCELLED,
                ]
                if status in line_statuses
            ]

            if len(set(line_statuses)) == 1:
                overall_status = line_statuses[0]
            else:
                overall_status = "Mixed"

            order_total = sum(line.get("total", 0) for line in order_lines)
            item_count = sum(line.get("quantity", 0) for line in order_lines)

            with st.container():
                st.markdown(f"#### Order {order_label}")
                cols = st.columns([3, 1])
                cols[0].markdown(f"**Items:** {item_count}")
                cols[0].markdown(f"**Order Total:** {format_price(order_total)}")
                cols[1].markdown(f"**Status:** {overall_status}")

                for status in unique_statuses:
                    status_lines = [line for line in order_lines if line.get("status") == status]
                    if not status_lines:
                        continue

                    st.markdown(f"**{status} Items**")
                    for line in status_lines:
                        line_total = line.get("price", 0) * line.get("quantity", 0)
                        if status == constants.ORDER_STATUS_CANCELLED:
                            st.markdown(
                                f"- ~~{line.get('item_name', 'Unknown')}~~ x {line.get('quantity', 0)} @ {format_price(line.get('price', 0))} = {format_price(line_total)} "
                                f"- {status}"
                            )
                        else:
                            st.markdown(
                                f"- {line.get('item_name', 'Unknown')} x {line.get('quantity', 0)} @ {format_price(line.get('price', 0))} = {format_price(line_total)} "
                                f"- {status}"
                            )

                if constants.ORDER_STATUS_CANCELLED in unique_statuses and constants.ORDER_STATUS_PLACED in unique_statuses:
                    st.info("Some items in this order were cancelled. Cancelled items are shown separately.")
                st.markdown("---")


    def cancel_order(self, user):
        st.subheader("Cancel Order")
        placed_orders = self.manager.find_placed_orders_by_customer(user["email"])

        if placed_orders == []:
            st.info("No orders to cancel.")

        else:
            selected_order = st.selectbox(
                "Select Order to Cancel",
                options=placed_orders,
                format_func=lambda order: f"{get_order_label(order)} — {order['item_name']} x {order['quantity']}"
            )

            if st.button(
                "Cancel Selected Order",
                key="cancel_order_btn",
                type="primary",
                use_container_width=True
            ):

                result = self.manager.cancel_order(selected_order["id"])

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
            st.rerun()

        for message in SessionStateManager.get_ai_messages():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input:
            messages = SessionStateManager.get_ai_messages()
            messages.append({
                "role": "user",
                "content": user_input
            })
            SessionStateManager.set_ai_messages(messages)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    ai_response = assistant.get_response(
                        SessionStateManager.get_ai_messages(),
                        user["email"]
                    )

                    st.markdown(ai_response)

            messages = SessionStateManager.get_ai_messages()
            messages.append({
                "role": "assistant",
                "content": ai_response
            })
            SessionStateManager.set_ai_messages(messages)

            logs = assistant.load_logs()
            logs.append({
                "user_email": user["email"],
                "user_message": user_input,
                "ai_response": ai_response
            })
            assistant.save_logs(logs)
