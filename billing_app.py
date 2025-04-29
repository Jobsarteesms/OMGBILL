import streamlit as st
import datetime

# --- Initialize products ---
if "products" not in st.session_state:
    st.session_state.products = [
        "Gingerly Oil", "Groundnut Oil", "Coconut Oil", "Cow Ghee",
        "Cow Butter", "Buffalo Butter", "Deebam Oil", "Vadagam"
    ]
if "new_product_added" not in st.session_state:
    st.session_state.new_product_added = False

# --- Handle reset before any widgets ---
if "reset" in st.session_state and st.session_state.reset:
    for product in st.session_state.products:
        st.session_state[f"{product}_qty"] = 0
        st.session_state[f"{product}_unit_type"] = ""
        st.session_state[f"{product}_price"] = 0.0
    st.session_state.reset = False
    st.experimental_rerun()

# --- Title and Date ---
st.title("🧾 Om Guru Store - Billing App")
st.write(f"📅 Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# --- Sidebar: Product Management ---
st.sidebar.header("🛠️ Manage Products")
new_product = st.sidebar.text_input("Add new product:")
if st.sidebar.button("Add Product"):
    if new_product and new_product not in st.session_state.products:
        st.session_state.products.append(new_product)
        st.session_state.new_product_added = True
        st.success(f"✅ Added: {new_product}")
    elif new_product in st.session_state.products:
        st.warning("⚠️ Product already exists.")
    else:
        st.error("❌ Please enter a valid product name.")

edit_product = st.sidebar.selectbox("Edit product:", st.session_state.products)
edited_name = st.sidebar.text_input("New name for selected product:")
if st.sidebar.button("Edit Selected Product"):
    if edited_name:
        idx = st.session_state.products.index(edit_product)
        st.session_state.products[idx] = edited_name
        st.success(f"✅ Updated: {edit_product} → {edited_name}")
        st.session_state.new_product_added = True
    else:
        st.warning("⚠️ Please enter a new name.")

delete_product = st.sidebar.selectbox("Delete product:", st.session_state.products)
if st.sidebar.button("Delete Selected Product"):
    st.session_state.products.remove(delete_product)
    st.success(f"🗑️ Deleted: {delete_product}")
    st.session_state.new_product_added = True

# Rerun if new product added
if st.session_state.new_product_added:
    st.session_state.new_product_added = False
    st.experimental_rerun()

# --- Product Entry Section ---
st.header("📦 Enter Product Details")
bill_items = {}

for product in st.session_state.products:
    qty_key = f"{product}_qty"
    unit_key = f"{product}_unit_type"
    price_key = f"{product}_price"

    if qty_key not in st.session_state:
        st.session_state[qty_key] = 0
    if unit_key not in st.session_state:
        st.session_state[unit_key] = ""
    if price_key not in st.session_state:
        st.session_state[price_key] = 0.0

    qty = st.number_input(f"{product} - Qty", min_value=0, step=1, key=qty_key)
    unit = st.text_input(f"{product} - Unit (g/L/kg)", key=unit_key)
    price = st.number_input(f"{product} - Price", min_value=0.0, step=0.5, key=price_key)

    if qty > 0 and price > 0:
        amt = qty * price
        bill_items[product] = (qty, unit, price, amt)

# --- Generate / Reset Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🧾 Generate Bill"):
        if not bill_items:
            st.warning("❗Please enter at least one item with price and quantity.")
        else:
            st.subheader("📋 Bill Summary")
            lines = []
            total = 0
            lines.append("🛒 Om Guru Store")
            lines.append(f"📅 Date: {datetime.date.today().strftime('%d-%m-%Y')}")
            lines.append("-" * 60)
            lines.append(f"{'Item':<20} {'Qty':>5} {'Unit':<6} {'Rate':>8} {'Amount':>10}")
            lines.append("-" * 60)

            for item, (qty, unit, rate, amt) in bill_items.items():
                lines.append(f"{item:<20} {qty:>5} {unit:<6} ₹{rate:>7.2f} ₹{amt:>8.2f}")
                total += amt

            lines.append("-" * 60)
            lines.append(f"{'Total':>45} ₹{total:>10.2f}")
            lines.append("-" * 60)
            lines.append("")
            lines.append("🙏 Thank you for your purchase!")

            bill_text = "\n".join(lines)
            st.text_area("📋 Copy & Share This Bill", value=bill_text, height=350)
            st.code(bill_text, language="text")
            st.info("✅ Long press to copy this bill and share on WhatsApp.")

with col2:
    if st.button("🔄 Reset Bill"):
        st.session_state.reset = True
        st.experimental_rerun()
