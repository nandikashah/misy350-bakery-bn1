import streamlit as st
import time
import uuid


class BakeryDashboard:
    def __init__(self, manager, inventory_store, user_store, order_store) -> None:
        self.manager = manager
        self.inventory_store = inventory_store
        self.user_store = user_store
        self.order_store = order_store

    def save_all(self):
        self.inventory_store.save(self.manager.inventory)
        self.user_store.save(self.manager.users)
        self.order_store.save(self.manager.orders)

    def main(self):
        if st.session_state["logged_in"]:
            if st.session_state["role"] == "Customer":
                self.customer_dashboard()
            elif st.session_state["role"] == "Owner":
                self.owner_dashboard()
        else:
            self.login_register()

        self.logout()

    # ---------------- LOGIN ----------------
    def login_register(self):
        st.subheader("Log In")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            user = self.manager.find_user(email, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["role"] = user["role"]
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.subheader("New Customer Account")

        name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            try:
                self.manager.register_customer(name, new_email, new_password)
                self.user_store.save(self.manager.users)
                st.success("Account created!")
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    # ---------------- CUSTOMER ----------------
    def customer_dashboard(self):
        user = st.session_state["user"]

        st.sidebar.markdown(f"## Welcome {user['full_name']}")
        st.sidebar.markdown(f"Cart Items: {len(st.session_state['cart'])}")

        if st.session_state.get("order_success"):
            st.success("Order placed successfully!")
            st.session_state["order_success"] = False

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Browse Items", "Cart", "My Orders", "Cancel Order"]
        )

        # -------- Browse --------
        with tab1:
            col1, col2 = st.columns([4, 2])

            with col1:
                inventory = self.manager.inventory

                selected_item = st.selectbox(
                    "Items",
                    options=inventory,
                    format_func=lambda item: item["name"]
                )

                quantity = st.number_input("Quantity", min_value=1)

                if st.button("Add to Cart"):
                    try:
                        self.manager.add_to_cart(
                            st.session_state["cart"], selected_item, quantity
                        )
                        st.success("Added to cart!")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))

            # -------- AI --------
            with col2:
                st.subheader("AI Assistant")

                for msg in st.session_state["messages"]:
                    with st.chat_message(msg["role"].lower()):
                        st.write(msg["content"])

                user_input = st.text_input("Ask a question:")

                if st.button("Send"):
                    if user_input:
                        st.session_state["messages"].append(
                            {"role": "User", "content": user_input}
                        )

                        if "order" in user_input.lower():
                            reply = "Add items to cart then checkout."
                        elif "cancel" in user_input.lower():
                            reply = "Use cancel tab."
                        else:
                            reply = "Try asking about orders."

                        st.session_state["messages"].append(
                            {"role": "Assistant", "content": reply}
                        )

                        st.rerun()

        # -------- Cart --------
        with tab2:
            cart = st.session_state["cart"]

            if not cart:
                st.info("Cart empty")
            else:
                total = 0
                for item in cart:
                    subtotal = item["price"] * item["quantity"]
                    total += subtotal
                    st.write(
                        f"{item['item_name']} | {item['quantity']} | ${subtotal}"
                    )

                st.write(f"Total: ${total}")

                if st.button("Checkout"):
                    user = st.session_state["user"]
                    self.manager.checkout(cart, user["email"])
                    self.save_all()
                    st.session_state["cart"] = []
                    st.session_state["order_success"] = True
                    st.rerun()

        # -------- Orders --------
        with tab3:
            user_orders = self.manager.find_orders_by_customer(user["email"])

            for order in user_orders:
                st.write(order)

        # -------- Cancel --------
        with tab4:
            orders = self.manager.find_placed_orders_by_customer(user["email"])
            ids = [o["id"] for o in orders]

            if ids:
                selected_id = st.selectbox("Select Order", ids)

                if st.button("Cancel"):
                    self.manager.cancel_order(selected_id)
                    self.save_all()
                    st.success("Cancelled")
                    st.rerun()

    # ---------------- OWNER ----------------
    def owner_dashboard(self):
        st.title("Owner Dashboard")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Orders", "Inventory", "Restock", "Update Status"]
        )

        with tab1:
            for order in self.manager.orders:
                st.write(order)

        with tab2:
            for item in self.manager.inventory:
                st.write(item)

        with tab3:
            names = [i["name"] for i in self.manager.inventory]
            selected = st.selectbox("Item", names)
            qty = st.number_input("Add Stock", min_value=1)

            if st.button("Restock"):
                self.manager.restock_inventory(selected, qty)
                self.inventory_store.save(self.manager.inventory)
                st.success("Stock updated!")
                st.rerun()

        with tab4:
            ids = [o["id"] for o in self.manager.orders]
            selected = st.selectbox("Order", ids)
            status = st.selectbox(
                "Status", ["Placed", "Completed", "Shipped", "Cancelled"]
            )

            if st.button("Update"):
                self.manager.update_order_status(selected, status)
                self.order_store.save(self.manager.orders)
                st.success("Updated!")
                st.rerun()

    # ---------------- LOGOUT ----------------
    def logout(self):
        if st.session_state["logged_in"]:
            if st.sidebar.button("Log out"):
                st.session_state["logged_in"] = False
                st.session_state["user"] = None
                st.session_state["role"] = None
                st.session_state["cart"] = []
                st.rerun()