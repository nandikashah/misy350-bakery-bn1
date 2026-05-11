import streamlit as st
import time


class OwnerDashboard:

    def __init__(self, manager) -> None:
        self.manager = manager


    def main(self):
        user = st.session_state["user"]

        total_orders = len(self.manager.orders)
        placed_orders = len([order for order in self.manager.orders if order["status"] == "Placed"])
        completed_orders = len([order for order in self.manager.orders if order["status"] == "Completed"])
        low_stock_items = len([item for item in self.manager.inventory if item["stock"] <= 5])

        st.sidebar.markdown(f"Logged in as: {user['full_name']} ({user['email']})")
        st.markdown(f"## Welcome, {user['full_name']}!")
        st.markdown("## Owner Dashboard")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Orders", total_orders)
        col2.metric("Placed", placed_orders)
        col3.metric("Completed", completed_orders)
        col4.metric("Low Stock", low_stock_items)

        tab1, tab2, tab3, tab4 = st.tabs([
            "View Orders",
            "View Inventory",
            "Restock Inventory",
            "Update Order Status"
        ])

        with tab1:
            self.view_orders()

        with tab2:
            self.view_inventory()

        with tab3:
            self.restock_inventory()

        with tab4:
            self.update_order_status()


    def view_orders(self):
        st.subheader("Orders Placed")

        if not self.manager.orders:
            st.info("No orders have been placed yet.")
            return

        st.table(self.manager.orders)


    def view_inventory(self):
        st.subheader("Inventory")

        if not self.manager.inventory:
            st.info("No inventory items available.")
            return

        st.table(self.manager.inventory)


    def restock_inventory(self):
        st.subheader("Restock Inventory")

        item_names = []

        for item in self.manager.inventory:
            item_names.append(item["name"])

        selected_item = st.selectbox("Select Item to Restock", item_names)
        stock_item = self.manager.find_item_by_name(selected_item)
        if stock_item:
            st.write(f"Current stock: {stock_item['stock']}")

        add_quantity = st.number_input("Add Amount", min_value=1, step=1)

        if st.button("Update Stock"):

            result = self.manager.restock_inventory(selected_item, add_quantity)

            if result == "Success":
                self.manager.save_inventory()

                st.success(f"Stock updated for {selected_item}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(result)


    def update_order_status(self):
        st.subheader("Update Order Status")

        col1, col2 = st.columns([3, 3])

        with col1:
            st.markdown("#### Orders Placed")

            for order in self.manager.orders:
                st.write("Order ID:", order["id"])
                st.write("Customer:", order["customer_email"])
                st.write("Item:", order["item_name"])
                st.write("Quantity:", order["quantity"])
                st.write("Status:", order["status"])
                st.write("---")

        with col2:
            st.markdown("#### Update Status")

            order_ids = []

            for order in self.manager.orders:
                order_ids.append(order["id"])

            selected_order = st.selectbox("Select Order to Update", order_ids, key="order_select")

            new_status = st.selectbox(
                "Select New Status",
                ["Placed", "Completed", "Shipped", "Cancelled"],
                key="new_status"
            )

            if st.button("Update Status", key="update_status"):

                result = self.manager.update_order_status(selected_order, new_status)

                if result == "Success":
                    self.manager.save_orders()

                    st.success("Order " + selected_order + " status updated to " + new_status + "!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result)