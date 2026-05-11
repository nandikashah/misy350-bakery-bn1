import streamlit as st
import time

from ui.state_manager import SessionStateManager
from shared import constants


class BakeryDashboard:
    
    def __init__(self, manager) -> None:
        self.manager = manager

    def _valid_email(self, email: str) -> bool:
        return "@" in email and "." in email

    def main(self):

        st.title("Blossom and Nandika's Bakery Delights")

        st.subheader("Log In")

        with st.container(border=True):
            email_input = st.text_input("Email", key="email_login")
            password_input = st.text_input("Password", type="password", key="password_login")

            if st.button("Log In", key="login_btn", type="primary", use_container_width=True):

                if email_input == "" or password_input == "":
                    st.error("Please enter both email and password")
                elif not self._valid_email(email_input):
                    st.error("Please enter a valid email address.")
                else:
                    with st.spinner("Logging in..."):
                        time.sleep(1)

                        found_user = self.manager.find_user(email_input, password_input)

                        if found_user:
                            st.success(f"Welcome, {found_user['full_name']}!")

                            SessionStateManager.set_logged_in(True)
                            SessionStateManager.set_user(found_user)
                            SessionStateManager.set_role(found_user["role"])

                            time.sleep(1)
                            st.rerun()

                        else:
                            st.error("Invalid credentials")


        st.subheader("New Customer Account")

        with st.container(border=True):
            new_full_name = st.text_input("Full Name", key="full_name_register")
            new_email = st.text_input("Email", key="email_register")
            new_password = st.text_input("Password", type="password", key="password_register")

            if st.button("Create Account", key="register_btn", type="primary", use_container_width=True):

                if not self._valid_email(new_email):
                    st.error("Please enter a valid email address.")
                else:
                    result = self.manager.register_customer(
                        new_full_name,
                        new_email,
                        new_password
                    )

                    if result == "Success":
                        self.manager.save_users()
                        st.success("Account created!")
                        st.session_state["full_name_register"] = ""
                        st.session_state["email_register"] = ""
                        st.session_state["password_register"] = ""
                        time.sleep(1)

                        st.rerun()
                    else:
                        st.error(result)