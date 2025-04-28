import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Initialize products
if 'products' not in st.session_state:
    st.session_state.products = [
        "Gingerly Oil", "Groundnut Oil", "Coconut Oil", "Cow Ghee",
        "Cow Butter", "Buffalo Butter", "Deebam Oil", "Vadagam"
    ]

# App title
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Add new product
new_product = st.text_input("Add a new product (optional):")
if new_product and new_product not in st.session_state.products:
    st.session_state.products.append(new_product)

# Edit and delete products
st.subheader("Manage Products")
product_to_edit = st.selectbox("Select a product to edit or delete", st.session_state.products)
edit_product = st.text_input("Edit product name:", value=product_to_edit)
if st.button("Save Changes"):
    if edit_product:
        idx = st.session_state.products.index(product_to_edit)
        st.session_state.products[idx] = edit_product
        st.success(f"Product '{product_to_edit}' has been updated to '{edit_product}'")

if st.button("Delete Product"):
    if product_to_edit:
        st.session_state.products.remove(product_to_edit)
        st.success(f"Product '{product_to_edit}' has been deleted")

st.header("Enter Product Details:")

# Input product quantities and prices
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
    bill_text.append(f"{'Product':30} {'Qty':>10} {'Unit Price':>15} {'Total':>15}")
    bill_text.append("-" * 60)
    for product, (qty, price, line_total) in bill_items.items():
        bill_text.append(f"{product:30} {qty:10} {price:15.2f} {line_total:15.2f}")
        total += line_total
    bill_text.append("-" * 60)
    bill_text.append(f"{'Total':50} {total:15.2f}")
    bill_text.append("-" * 60)

    bill_result = "\n".join(bill_text)
    st.text(bill_result)

    # --- Create Image ---
    img = create_bill_image(bill_result)

    # Save to buffer (WEBP - compressed)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="WEBP", quality=40)  # WEBP instead of JPEG
    img_buffer.seek(0)

    st.download_button(
        label="Download Compressed Bill as WEBP",
        data=img_buffer.getvalue(),
        file_name="bill.webp",
        mime="image/webp"
    )

# Share functionality using session state
if 'share_clicked' not in st.session_state:
    st.session_state.share_clicked = False

def show_share_options():
    st.session_state.share_clicked = True

# Share Button: Show only after click
if st.button("📤 Share Bill"):
    show_share_options()

if st.session_state.share_clicked:
    # Show Share Options after clicking "Share"
    st.markdown("### Choose How to Share:")

    # Share method selection
    share_option = st.selectbox("Select Share Method:", ["WhatsApp", "Gmail", "Others"])

    phone_or_email = st.text_input("Enter Phone (with country code) or Email:")

    if 'bill_result' in locals():
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

                else:  # Others
                    st.markdown("Copy this bill text and paste manually into other apps:")
                    st.code(bill_result)
    else:
        st.error("Please generate the bill first.")
