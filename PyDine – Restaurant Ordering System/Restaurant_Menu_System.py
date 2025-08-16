import streamlit as st
from datetime import datetime

# ---------------- MENU DATA ----------------
MENU = {
    'PIZZA': [('Cheese Pizza', 50), ('Veg Pizza', 60)],
    'PASTA': [('White Sauce Pasta', 70), ('Red Sauce Pasta', 65)],
    'BURGER': [('Veg Burger', 40), ('Aloo Tikki Burger', 45)],
    'SALAD': [('Green Salad', 30)],
    'COFFEE': [('Cold Coffee', 40), ('Warm Coffee', 20), ('Coffee Latte', 120), ('Filter Coffee', 135)],
    'ICECREAM': [('Chocolate Ice-Cream', 40), ('Vanilla Ice-Cream', 35), ('Strawberry Ice-Cream', 40), ('Black-Current', 40)]
}

# ---------------- SESSION STATE INIT ----------------
if "order_history" not in st.session_state:
    st.session_state.order_history = []
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# ---------------- FUNCTIONS ----------------
def add_to_order(main_item, sub_item, qty):
    name, price = sub_item
    st.session_state.order_history.append((name, qty, price))
    st.success(f"✅ Added {qty} x {name} to order.")

def print_receipt():
    total_amount = 0
    lines = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("========== BILL RECEIPT ==========")
    lines.append(f"Customer: {st.session_state.customer_name}")
    lines.append(f"Date & Time: {current_time}")
    lines.append("----------------------------------")

    for item, qty, price in st.session_state.order_history:
        item_total = qty * price
        total_amount += item_total
        lines.append(f"{item:<25} x{qty:<3} @ Rs {price:<4} = Rs {item_total}")

    discount = 0
    if total_amount > 500:
        discount = total_amount * 0.10
        lines.append(f"{'':>30}DISCOUNT (10%): -Rs {discount:.2f}")

    after_discount = total_amount - discount
    gst = after_discount * 0.18
    final_amount = after_discount + gst

    lines.append("----------------------------------")
    lines.append(f"{'':>30}GST (18%): Rs {gst:.2f}")
    lines.append(f"{'':>30}TOTAL TO PAY: Rs {final_amount:.2f}")
    lines.append("=========== THANK YOU ============")

    st.text("\n".join(lines))

# ---------------- UI ----------------
st.title("🍽️ Python Restaurant Ordering System")
st.subheader("Welcome! Please select items to place your order.")

# Customer Name
st.session_state.customer_name = st.text_input("Enter Customer Name:", st.session_state.customer_name)

# Menu Selection
main_item = st.selectbox("Select Main Category:", list(MENU.keys()))
sub_items = MENU[main_item]
sub_item = st.selectbox("Select Sub-Item:", sub_items, format_func=lambda x: f"{x[0]} - Rs {x[1]}")
qty = st.number_input("Quantity:", min_value=1, value=1)

# Add button
if st.button("Add to Order"):
    add_to_order(main_item, sub_item, qty)

# Show Current Order
if st.session_state.order_history:
    st.write("### 🛒 Current Order")
    for item, qty, price in st.session_state.order_history:
        st.write(f"- {item} x {qty} @ Rs {price} = Rs {qty * price}")

    if st.button("🧾 Generate Receipt"):
        print_receipt()
else:
    st.info("No items in order yet.")