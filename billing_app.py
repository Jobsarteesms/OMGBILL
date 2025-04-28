import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Initialize products
products = [
    "Gingerly Oil",
    "Groundnut Oil",
    "Coconut Oil",
    "Cow Ghee",
    "Cow Butter",
    "Buffalo Butter",
    "Deebam Oil",
    "Vadagam"
]

# App title
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Add new product
new_product = st.text_input("Add a new product (optional):")
if new_product:
    products.append(new_product)

st.header("Enter Product Details:")

# Input product quantities and prices
bill_items = {}
for product in products:
    qty = st.number_input(f"{product} - Quantity", min_value=0, step=1, key=f"{product}_qty")
    price_per_unit = st.number_input(f"{product} - Price per unit", min_value=0.0, step=0.5, key=f"{product}_price")
    if qty > 0 and price_per_unit > 0:
        total_price = qty * price_per_unit
        bill_items[product] = (qty, price_per_unit, total_price)

# Function to create JPG from bill
def create_bill_image(bill_text):
    # Create blank white image
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)

    # Set font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Write text
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
    bill_text.append("-" * 40)
    bill_text.append(f"{'Product':20} {'Qty':>5} {'Unit':>6} {'Total':>8}")
    bill_text.append("-" * 40)
    for product, (qty, price, line_total) in bill_items.items():
        bill_text.append(f"{product:20} {qty:5} {price:6.2f} {line_total:8.2f}")
        total += line_total
    bill_text.append("-" * 40)
    bill_text.append(f"{'Total':30} {total:8.2f}")
    bill_text.append("-" * 40)

    bill_result = "\n".join(bill_text)
    st.text(bill_result)

    # --- Create JPG Image ---
    img = create_bill_image(bill_result)
    
    # Save to buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG")
    img_buffer.seek(0)

    st.download_button(
        label="Download Bill as JPG",
        data=img_buffer,
        file_name="bill.jpg",
        mime="image/jpeg"
    )

    # --- WhatsApp Share Section ---
    st.markdown("### 📲 Share on WhatsApp")

    phone_number = st.text_input("Enter WhatsApp Number (with country code, e.g., +91...)")

    message = bill_result.replace(' ', '%20').replace('\n', '%0A')  # WhatsApp formatting
    if st.button("Generate WhatsApp Link"):
        if phone_number:
            whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={message}"
            st.markdown(f"[Click here to Share on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)
        else:
            st.error("Please enter a valid phone number.")

    st.info("📱 Tip: After clicking the link, you can choose the contact from your WhatsApp app.")
