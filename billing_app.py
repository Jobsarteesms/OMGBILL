import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Initialize session state for products
if "products" not in st.session_state:
    st.session_state.products = [
        "Gingerly Oil", "Groundnut Oil", "Coconut Oil", "Cow Ghee",
        "Cow Butter", "Buffalo Butter", "Deebam Oil", "Vadagam"
    ]

products = st.session_state.products

# App title
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Add new product
st.subheader("➕ Add New Product")
new_product = st.text_input("Enter new product name:")
if st.button("Add Product"):
    if new_product and new_product not in products:
        products.append(new_product)
        st.success(f"Added product: {new_product}")
        st.experimental_rerun()
    elif new_product in products:
        st.warning("Product already exists.")
    else:
        st.error("Please enter a valid product name.")

# Edit or delete product
st.subheader("✏️ Edit or Delete Product")
if products:
    product_to_edit = st.selectbox("Select product to edit/delete:", products)
    new_name = st.text_input("Edit product name:", value=product_to_edit)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Product Name"):
            if new_name and new_name != product_to_edit:
                idx = products.index(product_to_edit)
                products[idx] = new_name
                st.success(f"Updated product name to: {new_name}")
                st.experimental_rerun()
    with col2:
        if st.button("Delete Product"):
            products.remove(product_to_edit)
            st.success(f"Deleted product: {product_to_edit}")
            st.experimental_rerun()
else:
    st.warning("No products available.")

st.header("Enter Product Details:")

# Input product quantities and prices
bill_items = {}
for product in products:
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        qty = st.number_input(f"{product} - Unit Numbers", min_value=0, step=1, key=f"{product}_qty")
    with col2:
        unit_label = st.text_input(f"{product} - Units (e.g. gm/ltr)", key=f"{product}_unit")
    with col3:
        price_per_unit = st.number_input(f"{product} - Price per unit", min_value=0.0, step=0.5, key=f"{product}_price")

    if qty > 0 and price_per_unit > 0:
        total_price = qty * price_per_unit
        bill_items[product] = (qty, unit_label, price_per_unit, total_price)

# Function to create Image from bill
def create_bill_image(bill_text):
    lines = bill_text.count('\n') + 1
    height = max(1000, 40 * lines)
    width = 800

    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    y_text = 20
    for line in bill_text.split('\n'):
        d.text((40, y_text), line, font=font, fill=(0, 0, 0))
        y_text += 30

    return img

# Generate Bill
if st.button("Generate Bill"):
    st.subheader("🧾 Bill Summary:")
    total = 0
    bill_text = []
    bill_text.append(f"------ Om Guru Store ------")
    bill_text.append(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    bill_text.append("-" * 60)
    bill_text.append(f"{'Product':20} {'Qty':>5} {'Unit':>8} {'Price':>7} {'Total':>8}")
    bill_text.append("-" * 60)
    for product, (qty, unit_label, price, line_total) in bill_items.items():
        bill_text.append(f"{product:20} {qty:5} {unit_label:>8} {price:7.2f} {line_total:8.2f}")
        total += line_total
    bill_text.append("-" * 60)
    bill_text.append(f"{'Total':>45} {total:8.2f}")
    bill_text.append("-" * 60)

    bill_result = "\n".join(bill_text)
    st.text(bill_result)

    # Create Image
    img = create_bill_image(bill_result)

    # Save to buffer (WEBP - compressed)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="WEBP", quality=40)
    img_buffer.seek(0)

    st.download_button(
        label="Download Compressed Bill as WEBP",
        data=img_buffer.getvalue(),
        file_name="bill.webp",
        mime="image/webp"
    )

    # Share Option
    if st.button("📤 Share Bill"):
        st.markdown("### Choose How to Share:")
        share_option = st.selectbox("Select Share Method:", ["WhatsApp", "Gmail", "Others"])
        phone_or_email = st.text_input("Enter Phone (with country code) or Email:")

        share_message = bill_result.replace(' ', '%20').replace('\n', '%0A')

        if st.button("Generate Share Link"):
            if not phone_or_email:
                st.error("Please enter a Phone number or Email address.")
            else:
                if share_option == "WhatsApp":
                    whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_or_email}&text={share_message}"
                    st.markdown(f"[Click here to Share on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)

                elif share_option == "Gmail":
                    gmail_url = f"mailto:{phone_or_email}?subject=Om%20Guru%20Store%20Bill&body={share_message}"
                    st.markdown(f"[Click here to Share via Gmail]({gmail_url})", unsafe_allow_html=True)

                else:
                    st.markdown("Copy this bill text and paste manually into other apps:")
                    st.code(bill_result)
