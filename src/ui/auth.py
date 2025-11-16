# src/ui/auth.py
import streamlit as st
import os
import json
import hashlib

USERS_FILE = "data/users.json"

# --- Helper Functions ---
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Authentication Page ---
def auth_page():
    st.title("🔐 User Authentication")

    tab1, tab2 = st.tabs(["🔑 Login", "🧾 Register"])

    # --- LOGIN TAB ---
    with tab1:
        st.subheader("Login to KnowMap")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            users = load_users()
            if username in users and users[username]["password"] == hash_password(password):
                st.session_state["auth_user"] = username
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    # --- REGISTER TAB ---
    with tab2:
        st.subheader("Create New Account")
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Register"):
            if not new_user or not new_pass:
                st.warning("Please fill all fields")
            elif new_pass != confirm_pass:
                st.warning("Passwords do not match")
            else:
                users = load_users()
                if new_user in users:
                    st.warning("Username already exists")
                else:
                    users[new_user] = {"password": hash_password(new_pass)}
                    save_users(users)
                    st.success("✅ Registration successful! You can now log in.")
