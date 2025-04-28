import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Initialize predefined products (auto display)
predefined_products = [
    "Apple", "Banana", "Milk", "Rice", "Wheat Flour", "Sugar", "Salt", "Tea"
]

# Store selected products and their details
if 'products' not in st.session_state:
    st.session_state.products = {product: {"qty_type": "", "num_pieces": 0, "price_per_piece": 0.0} for product in predefined_products}

# App title
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Input fields for products
st.header("Enter Product Details:")

bill_items = {}
for product in st.session_state.products:
    qty_type = st.text_input(f"Quantity Type for {product} (e.g., 500g, 1 liter):", key=f"{product}_qty_type")
    num_pieces = st.number_input(f"Number of Pieces for {product} (e.g., 1, 5):", min_value=0, step=1, key=f"{product}_pieces")
    price_per_piece = st.number_input(f"Price per Piece for {product} (₹):", min_value=0.0, step=0.5, key=f"{product}_price")

    # Store user inputs
    if qty_type and num_pieces > 0 and price_per_piece > 0:
        total_price = num_pieces * price_per_piece
        bill_items[product] = {"qty_type": qty_type, "num_pieces": num_pieces, "price_per_piece": price_per_piece, "total_price": total_price}

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
    bill_text.append(f"{'Product Name':30} {'Qty Type':>15} {'Qty':>10} {'Price per Piece':>20} {'Total':>15}")
    bill_text.append("-" * 80)

    for product_name, details in bill_items.items():
        qty_type = details["qty_type"]
        num_pieces = details["num_pieces"]
        price_per_piece = details["price_per_piece"]
        line_total = details["total_price"]
        bill_text.append(f"{product_name:30} {qty_type:15} {num_pieces:10} {price_per_piece:20.2f} {line_total:15.2f}")
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
