import streamlit as st
import time

from shared import constants
from shared.utils import format_price, get_order_label


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

        grouped_orders = {}
        for order in self.manager.orders:
            label = get_order_label(order)
            grouped_orders.setdefault(label, []).append(order)

        for order_label, order_lines in grouped_orders.items():
            line_statuses = [line.get("status", "Unknown") for line in order_lines]
            if len(set(line_statuses)) == 1:
                overall_status = line_statuses[0]
            else:
                overall_status = "Mixed"

            order_total = sum(line.get("total", 0) for line in order_lines)
            item_count = sum(line.get("quantity", 0) for line in order_lines)

            with st.container():
                st.markdown(f"#### Order {order_label}")
                cols = st.columns([3, 1])
                cols[0].markdown(f"**Customer:** {order_lines[0].get('customer_email', 'Unknown')}")
                cols[0].markdown(f"**Items:** {item_count}")
                cols[1].markdown(f"**Status:** {overall_status}")
                cols[1].markdown(f"**Total:** {format_price(order_total)}")

                for line in order_lines:
                    line_total = line.get("total", 0)
                    st.markdown(
                        f"- {line.get('item_name', 'Unknown')} x {line.get('quantity', 0)} = {format_price(line_total)} "
                        f"({line.get('status', 'Unknown')})"
                    )

                st.markdown("---")


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
            st.markdown("#### Orders Overview")

            if not self.manager.orders:
                st.info("No orders to display.")
            else:
                grouped_orders = {}
                for order in self.manager.orders:
                    label = get_order_label(order)
                    grouped_orders.setdefault(label, []).append(order)

                for order_label, order_lines in grouped_orders.items():
                    line_statuses = [line.get("status", "Unknown") for line in order_lines]
                    if len(set(line_statuses)) == 1:
                        overall_status = line_statuses[0]
                    else:
                        overall_status = "Mixed"

                    with st.expander(f"Order {order_label} — {overall_status}"):
                        for line in order_lines:
                            st.markdown(
                                f"- {line.get('item_name', 'Unknown')} x {line.get('quantity', 0)} "
                                f"({line.get('status', 'Unknown')})"
                            )

        with col2:
            st.markdown("#### Update Status")
            st.info("Shipped, Completed, and Cancelled orders are final and locked.")

            editable_orders = [
                order for order in self.manager.orders
                if order.get("status") == constants.ORDER_STATUS_PLACED
            ]

            if not editable_orders:
                st.info("No editable orders are available at this time.")
                return

            selected_order = st.selectbox(
                "Select Order to Update",
                options=editable_orders,
                format_func=lambda order: f"{get_order_label(order)} — {order['item_name']} x {order['quantity']}",
                key="order_select"
            )

            new_status = st.selectbox(
                "Select New Status",
                options=constants.ORDER_STATUS_TRANSITIONS.get(constants.ORDER_STATUS_PLACED, []),
                key="new_status"
            )

            if st.button("Update Status", key="update_status"):
                result = self.manager.update_order_status(selected_order["id"], new_status)

                if result == "Success":
                    self.manager.save_orders()
                    st.success(f"Order {get_order_label(selected_order)} status updated to {new_status}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result)