import json
import random
import string
from pathlib import Path
import streamlit as st


class Bank:
    DATABASE = "data.json"

    def __init__(self):
        self.data = self.load_data()
        self.migrate_data()   # 🔥 auto fix old data

    def load_data(self):
        if Path(self.DATABASE).exists():
            try:
                with open(self.DATABASE, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        with open(self.DATABASE, "w") as f:
            json.dump(self.data, f, indent=4)

    # 🔥 AUTO FIX OLD DATA
    def migrate_data(self):
        updated = False

        for user in self.data:
            # accountNo. → account
            if "accountNo." in user:
                user["account"] = user.pop("accountNo.")
                updated = True

            # ballance → balance
            if "ballance" in user:
                user["balance"] = user.pop("ballance")
                updated = True

            # ensure balance exists
            if "balance" not in user:
                user["balance"] = 0
                updated = True

            # pin always string
            if "pin" in user:
                user["pin"] = str(user["pin"])

        if updated:
            self.save_data()

    def generate_account(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def find_user(self, acc, pin):
        for user in self.data:
            acc_key = user.get("account") or user.get("accountNo.")
            if acc_key == acc and str(user.get("pin")) == str(pin):
                return user
        return None

    def create(self, name, age, email, pin):
        if age < 18:
            return False, "Age must be 18+"
        if len(pin) != 4 or not pin.isdigit():
            return False, "PIN must be 4 digits"

        acc = self.generate_account()

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account": acc,
            "balance": 0
        }

        self.data.append(user)
        self.save_data()
        return True, user

    def deposit(self, acc, pin, amt):
        user = self.find_user(acc, pin)
        if not user:
            return False, "Invalid details"

        if amt <= 0 or amt > 10000:
            return False, "Amount must be between 1 and 10000"

        user["balance"] = user.get("balance", 0) + amt
        self.save_data()
        return True, f"Balance: {user['balance']}"

    def withdraw(self, acc, pin, amt):
        user = self.find_user(acc, pin)
        if not user:
            return False, "Invalid details"

        if amt > user.get("balance", 0):
            return False, "Insufficient balance"

        user["balance"] -= amt
        self.save_data()
        return True, f"Balance: {user['balance']}"

    def get(self, acc, pin):
        user = self.find_user(acc, pin)
        if not user:
            return False, "Invalid details"
        return True, user

    def update(self, acc, pin, name, email, new_pin):
        user = self.find_user(acc, pin)
        if not user:
            return False, "Invalid details"

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if new_pin:
            if len(new_pin) != 4 or not new_pin.isdigit():
                return False, "PIN must be 4 digits"
            user["pin"] = new_pin

        self.save_data()
        return True, "Updated successfully"

    def delete(self, acc, pin):
        user = self.find_user(acc, pin)
        if not user:
            return False, "Invalid details"

        self.data.remove(user)
        self.save_data()
        return True, "Deleted successfully"


# ---------------- STREAMLIT ----------------

st.set_page_config(page_title="Bank App", page_icon="🏦")
st.title("🏦 Bank Management System")

bank = Bank()

menu = ["Create", "Deposit", "Withdraw", "Details", "Update", "Delete"]
choice = st.sidebar.selectbox("Menu", menu)


# CREATE
if choice == "Create":
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100)
    email = st.text_input("Email")
    pin = st.text_input("PIN", type="password")

    if st.button("Create"):
        ok, res = bank.create(name, age, email, pin)

        if ok:
            st.success("Account Created")
            st.json(res)
        else:
            st.error(res)


# DEPOSIT
elif choice == "Deposit":
    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", 1)

    if st.button("Deposit"):
        ok, msg = bank.deposit(acc, pin, amt)

        if ok:
            st.success(msg)
        else:
            st.error(msg)


# WITHDRAW
elif choice == "Withdraw":
    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", 1)

    if st.button("Withdraw"):
        ok, msg = bank.withdraw(acc, pin, amt)

        if ok:
            st.success(msg)
        else:
            st.error(msg)


# DETAILS
elif choice == "Details":
    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        ok, res = bank.get(acc, pin)

        if ok:
            res.pop("pin", None)
            st.json(res)
        else:
            st.error(res)


# UPDATE
elif choice == "Update":
    acc = st.text_input("Account No")
    pin = st.text_input("Old PIN", type="password")
    name = st.text_input("New Name")
    email = st.text_input("New Email")
    new_pin = st.text_input("New PIN", type="password")

    if st.button("Update"):
        ok, msg = bank.update(acc, pin, name, email, new_pin)

        if ok:
            st.success(msg)
        else:
            st.error(msg)


# DELETE
elif choice == "Delete":
    acc = st.text_input("Account No")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        ok, msg = bank.delete(acc, pin)

        if ok:
            st.success(msg)
        else:
            st.error(msg)