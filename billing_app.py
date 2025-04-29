import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import pyperclip  # Added for clipboard functionality

# --- Initialize session state ---
if "products" not in st.session_state:
    st.session_state.products = [
        "Gingerly Oil", "Groundnut Oil", "Coconut Oil", "Cow Ghee",
        "Cow Butter", "Buffalo Butter", "Deebam Oil", "Vadagam"
    ]
if "new_product_added" not in st.session_state:
    st.session_state.new_product_added = False

# --- App Title ---
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# --- Add/Edit/Delete Products ---
st.sidebar.header("🛠️ Manage Products")

# Add product
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

# Edit product
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

# Delete product
delete_product = st.sidebar.selectbox("Delete product:", options=st.session_state.products)
if st.sidebar.button("Delete Selected Product"):
    st.session_state.products.remove(delete_product)
    st.success(f"Deleted: {delete_product}")
    st.session_state.new_product_added = True

# Handle safe rerun
if st.session_state.get("new_product_added"):
    st.session_state.new_product_added = False
    st.experimental_rerun()

# --- Product Entry Section ---
st.header("Enter Product Details:")

bill_items = {}
for product in st.session_state.products:
    qty = st.number_input(f"{product} - Unit Numbers", min_value=0, step=1, key=f"{product}_qty")
    unit_type = st.text_input(f"{product} - Unit Type (e.g., grams/liters)", key=f"{product}_unit_type")
    price_per_unit = st.number_input(f"{product} - Price per unit", min_value=0.0, step=0.5, key=f"{product}_price")

    if qty > 0 and price_per_unit > 0:
        total_price = qty * price_per_unit
        bill_items[product] = (qty, unit_type, price_per_unit, total_price)

# --- Generate Image Bill ---
def create_bill_image(bill_text):
    lines = bill_text.count('\n') + 1
    height = max(1000, 40 * lines)
    width = 850

    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    y = 20
    for line in bill_text.split('\n'):
        draw.text((40, y), line, font=font, fill=(0, 0, 0))
        y += 30

    return img

# --- Generate Bill Button ---
if st.button("Generate Bill"):
    st.subheader("🧾 Bill Summary")
    total = 0
    bill_text = []
    bill_text.append("------ Om Guru Store ------")
    bill_text.append(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    bill_text.append("-" * 80)
    bill_text.append(f"{'Product':20} {'Qty':>5} {'Unit':>10} {'Price':>8} {'Total':>10}")
    bill_text.append("-" * 80)

    for product, (qty, unit_type, price, line_total) in bill_items.items():
        bill_text.append(f"{product:20} {qty:5} {unit_type:10} {price:8.2f} {line_total:10.2f}")
        total += line_total

    bill_text.append("-" * 80)
    bill_text.append(f"{'Total':>55} {total:10.2f}")
    bill_text.append("-" * 80)

    result = "\n".join(bill_text)
    st.text(result)

    # Generate and display image
    img = create_bill_image(result)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="WEBP", quality=40)
    img_buffer.seek(0)

    st.download_button(
        label="Download Compressed Bill as WEBP",
        data=img_buffer.getvalue(),
        file_name="bill.webp",
        mime="image/webp"
    )

    # --- Updated Share Option ---
    st.subheader("📤 Share Bill")

    bill_text_to_share = result

    # Copy to Clipboard Button
    if st.button("Copy Bill to Clipboard"):
        try:
            pyperclip.copy(bill_text_to_share)
            st.success("Bill copied to clipboard! Now open WhatsApp, Email or Messages and Paste.")
        except Exception as e:
            st.warning("Copying not supported in this environment. Please manually copy below.")

    # Always show text area for manual copy
    st.text_area("Bill Text (Copy manually if needed):", bill_text_to_share, height=300)

    st.markdown("### 📱 Choose an App to Paste the Bill:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[![WhatsApp](https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg)](https://wa.me/)", unsafe_allow_html=True)
        st.caption("Open WhatsApp")

    with col2:
        st.markdown("[![Gmail](https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png)](mailto:)", unsafe_allow_html=True)
        st.caption("Open Gmail")

    with col3:
        st.markdown("[![Messages](https://upload.wikimedia.org/wikipedia/commons/8/83/SMS_Icon.png)](sms:)", unsafe_allow_html=True)
        st.caption("Open SMS/Messages")

    st.info("✅ After copying, open your favorite app, paste the bill text and send it.")
