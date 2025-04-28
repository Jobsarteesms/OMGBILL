import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Initialize products
if 'products' not in st.session_state:
    st.session_state.products = []

# App title
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Add new product
new_product = st.text_input("Add a new product (optional):")
if new_product:
    if new_product not in st.session_state.products:
        st.session_state.products.append(new_product)

# Input fields for products
st.header("Enter Product Details:")

bill_items = {}
for product in st.session_state.products:
    qty = st.number_input(f"{product} - Quantity", min_value=0, step=1, key=f"{product}_qty")
    price_per_unit = st.number_input(f"{product} - Price per unit", min_value=0.0, step=0.5, key=f"{product}_price")
    if qty > 0 and price_per_unit > 0:
        total_price = qty * price_per_unit
        bill_items[product] = (qty, price_per_unit, total_price)

# Function to create Image from bill
def create_bill_image(bill_text):
    lines = bill_text.count('\n') + 1
    height = max(1000, 40 * lines)
    width = 1000

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
if st.button("Generate & Share Bill"):
    st.subheader("🧾 Bill Summary:")
    total = 0
    bill_text = []
    bill_text.append(f"------ Om Guru Store ------")
    bill_text.append(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    bill_text.append("-" * 80)
    bill_text.append(f"{'Product':30} {'Qty':>10} {'Unit Price':>15} {'Total':>15}")
    bill_text.append("-" * 80)
    for product, (qty, price, line_total) in bill_items.items():
        bill_text.append(f"{product:30} {qty:10} {price:15.2f} {line_total:15.2f}")
        total += line_total
    bill_text.append("-" * 80)
    bill_text.append(f"{'Total':50} {total:15.2f}")
    bill_text.append("-" * 80)

    bill_result = "\n".join(bill_text)
    st.text(bill_result)

    # --- Create Image ---
    img = create_bill_image(bill_result)

    # Save to buffer (WEBP - compressed)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="WEBP", quality=40)  # WEBP instead of JPEG
    img_buffer.seek(0)

    # Show Share Options after click
    share_option = st.selectbox("Select Share Method:", ["WhatsApp", "Gmail", "Copy Text"])

    # Collect phone/email for sharing
    phone_or_email = st.text_input("Enter Phone (with country code) or Email:")

    # Generate Shareable Link
    if st.button("Generate Share Link"):
        if not phone_or_email:
            st.error("Please enter a Phone number or Email address.")
        else:
            if share_option == "WhatsApp":
                whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_or_email}&text={bill_result}"
                st.markdown(f"[Click here to Share on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)

            elif share_option == "Gmail":
                gmail_url = f"mailto:{phone_or_email}?subject=Om%20Guru%20Store%20Bill&body={bill_result}"
                st.markdown(f"[Click here to Share via Gmail]({gmail_url})", unsafe_allow_html=True)

            elif share_option == "Copy Text":
                st.markdown("Copy this bill text and paste manually into other apps:")
                st.code(bill_result)

    # If user does not want to share, show download button
    st.download_button(
        label="Download Compressed Bill as WEBP",
        data=img_buffer.getvalue(),
        file_name="bill.webp",
        mime="image/webp"
    )
