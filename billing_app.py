import streamlit as st
import datetime

# --- Initialize session state ---
if "products" not in st.session_state:
    st.session_state.products = [
        "Gingerly Oil", "Groundnut Oil", "Coconut Oil", "Cow Ghee",
        "Cow Butter", "Buffalo Butter", "Deebam Oil", "Vadagam"
    ]
if "new_product_added" not in st.session_state:
    st.session_state.new_product_added = False

# --- Title ---
st.title("🧾 Om Guru Store - Billing App")
st.write(f"📅 Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# --- Sidebar for product management ---
st.sidebar.header("🛠️ Manage Products")
new_product = st.sidebar.text_input("Add new product:")
if st.sidebar.button("Add Product"):
    if new_product and new_product not in st.session_state.products:
        st.session_state.products.append(new_product)
        st.session_state.new_product_added = True
        st.success(f"Added: {new_product}")
    elif new_product in st.session_state.products:
        st.warning("Product already exists.")
    else:
        st.error("Enter a valid product name.")

edit_product = st.sidebar.selectbox("Edit product:", options=st.session_state.products)
edited_name = st.sidebar.text_input("New name for selected product:")
if st.sidebar.button("Edit Selected Product"):
    if edited_name:
        idx = st.session_state.products.index(edit_product)
        st.session_state.products[idx] = edited_name
        st.success(f"Updated: {edit_product} to {edited_name}")
        st.session_state.new_product_added = True
    else:
        st.warning("Please enter a new name.")

delete_product = st.sidebar.selectbox("Delete product:", options=st.session_state.products)
if st.sidebar.button("Delete Selected Product"):
    st.session_state.products.remove(delete_product)
    st.success(f"Deleted: {delete_product}")
    st.session_state.new_product_added = True

# Rerun after product update
if st.session_state.new_product_added:
    st.session_state.new_product_added = False
    st.experimental_rerun()

# --- Product Inputs ---
st.header("📦 Enter Product Details")

bill_items = {}
for product in st.session_state.products:
    qty = st.number_input(f"{product} - Qty", min_value=0, step=1, key=f"{product}_qty")
    unit_type = st.text_input(f"{product} - Unit (e.g., g/L)", key=f"{product}_unit_type")
    price_per_unit = st.number_input(f"{product} - Price", min_value=0.0, step=0.5, key=f"{product}_price")

    if qty > 0 and price_per_unit > 0:
        line_total = qty * price_per_unit
        bill_items[product] = (qty, unit_type, price_per_unit, line_total)

# --- Bill Generation ---
if st.button("Generate Bill"):
    st.subheader("🧾 Bill Summary")

    total = 0
    lines = []
    lines.append("🛒 Om Guru Store")
    lines.append(f"📅 Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    lines.append("-" * 40)
    lines.append(f"{'Item':15} {'Qty':>4} {'Unit':>5} {'Rate':>6} {'Amt':>7}")
    lines.append("-" * 40)

    for product, (qty, unit, rate, amt) in bill_items.items():
        lines.append(f"{product[:15]:15} {qty:>4} {unit[:5]:>5} {rate:>6.2f} {amt:>7.2f}")
        total += amt

    lines.append("-" * 40)
    lines.append(f"{'Total':>31} ₹ {total:>7.2f}")
    lines.append("-" * 40)

    bill_text = "\n".join(lines)

    # Show bill text
    st.text_area("📋 Bill Text (Long press to copy)", value=bill_text, height=300)

    # Copy to clipboard
    st.code(bill_text, language="text")
    st.info("✅ Long press to select and copy. Then share via WhatsApp, Email, etc.")
