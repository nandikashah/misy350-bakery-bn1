import streamlit as st
from pathlib import Path

from data.bakery_store import BakeryStore
from services.bakery_manager import BakeryManager

from ui.bakery_dashboard import BakeryDashboard
from ui.customer_dashboard import CustomerDashboard
from ui.owner_dashboard import OwnerDashboard
from ui.state_manager import SessionStateManager

from shared import constants


st.set_page_config(
    page_title="Blossom and Nandika's Bakery Delights",
    layout="centered",
    initial_sidebar_state="expanded"
)

# WITH HELP FROM AI TO CREATE A MORE AESTHETICALLY PLEASING UI
st.markdown("""
<style>

/* App background */
.stApp {
    background: linear-gradient(135deg, #fff7f0 0%, #ffe8df 45%, #e8fff5 100%);
}

/* Main content spacing */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #f47c6b;
    font-family: "Trebuchet MS", sans-serif;
}

/* Main cards / containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(255, 255, 255, 0.92);
    border: 2px solid #ffc9bd;
    border-radius: 26px;
    box-shadow: 0 8px 24px rgba(244, 124, 107, 0.12);
    padding: 14px;
}

/* Buttons */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #ff9a8b, #8ee6c4);
    color: white;
    border: none;
    border-radius: 18px;
    padding: 0.7rem 1rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(255, 154, 139, 0.25);
}

[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #ff7f6e, #75dcb9);
    color: white;
    transform: scale(1.02);
}

/* Inputs */
.stTextInput input,
[data-testid="stNumberInput"] input {
    background-color: white !important;
    border: 2px solid #ffd2c8 !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

/* Select boxes */
[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 14px !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 700;
    color: #555;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ff7f6e;
    border-bottom: 3px solid #ff7f6e;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffe3dc, #e0fff2);
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ff7f6e;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 18px;
    padding: 10px;
    border: 1px solid #ffd2c8;
}

/* Hide default header */
header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
<div style="
    background: linear-gradient(135deg, #ff9a8b, #8ee6c4);
    padding: 34px;
    border-radius: 30px;
    color: white;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 10px 28px rgba(244, 124, 107, 0.18);
">
    <h1 style="color:white; font-size:44px; margin-bottom:10px;">
        🍰 Blossom & Nandika's Bakery Delights
    </h1>
    <p style="font-size:20px; color:white; margin:0;">
        Sweet treats for sweeter prices ✨
    </p>
</div>
""",
    unsafe_allow_html=True
)

# SESSION STATES - Centralized initialization via SessionStateManager
SessionStateManager.initialize()


# Data & Object Handler
store = BakeryStore(Path("data"))
manager = BakeryManager(store)


# Handling Pages
if not SessionStateManager.get_logged_in():
    bakery_dashboard = BakeryDashboard(manager)
    bakery_dashboard.main()

else:
    if SessionStateManager.get_role() == constants.USER_ROLE_CUSTOMER:
        customer_dashboard = CustomerDashboard(manager)
        customer_dashboard.main()

    elif SessionStateManager.get_role() == constants.USER_ROLE_OWNER:
        owner_dashboard = OwnerDashboard(manager)
        owner_dashboard.main()





# Log Out
if SessionStateManager.get_logged_in():
    if st.sidebar.button("Log out", type="primary", use_container_width=True):
        SessionStateManager.reset_on_logout()
        st.rerun()