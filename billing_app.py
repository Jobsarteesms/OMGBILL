import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Store selected products and their details
if 'products' not in st.session_state:
    st.session_state.products = []

# App title
st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Input fields for adding products
st.header("Enter Product Details:")

# Form to add a new product
with st.form(key="product_form"):
    product_name = st.text_input("Product Name:")
    qty_type = st.text_input("Quantity Type (e.g., 500g, 1 liter):")
    num_pieces = st.number_input("Number of Pieces (e.g., 1, 5):", min_value=0, step=1)
    price_per_piece = st.number_input("Price per Piece (₹):", min_value=0.0, step=0.5)

    # Submit button to add product
    submit_button = st.form_submit_button(label="Add Product")

    if submit_button and product_name and qty_type and num_pieces > 0 and price_per_piece > 0:
        # Add product to the session state list
        st.session_state.products.append({
            "product_name": product_name,
            "qty_type": qty_type,
            "num_pieces": num_pieces,
            "price_per_piece": price_per_piece
        })
        st.success(f"Product '{product_name}' added successfully!")

# Display current product list with options to edit or delete
if st.session_state.products:
    st.subheader("Current Products:")
    for i, product in enumerate(st.session_state.products):
        product_name = product["product_name"]
        qty_type = product["qty_type"]
        num_pieces = product["num_pieces"]
        price_per_piece = product["price_per_piece"]
        total_price = num_pieces * price_per_piece

        # Display product details
        st.write(f"**{product_name}** - {qty_type} - {num_pieces} pieces - ₹{price_per_piece:.2f} each - Total: ₹{total_price:.2f}")

        # Edit or Delete buttons
        col1, col2 = st.columns(2)
        with col1:
            edit_button = st.button("Edit", key=f"edit_{i}")
        with col2:
            delete_button = st.button("Delete", key=f"delete_{i}")

        if edit_button:
            # Allow editing the selected product's details
            new_product_name = st.text_input(f"Edit Product Name (Current: {product_name}):", value=product_name)
            new_qty_type = st.text_input(f"Edit Quantity Type (Current: {qty_type}):", value=qty_type)
            new_num_pieces = st.number_input(f"Edit Number of Pieces (Current: {num_pieces}):", min_value=0, step=1, value=num_pieces)
            new_price_per_piece = st.number_input(f"Edit Price per Piece (Current: ₹{price_per_piece}):", min_value=0.0, step=0.5, value=price_per_piece)

            if st.button(f"Save Edit for {product_name}", key=f"save_edit_{i}"):
                st.session_state.products[i] = {
                    "product_name": new_product_name,
                    "qty_type": new_qty_type,
                    "num_pieces": new_num_pieces,
                    "price_per_piece": new_price_per_piece
                }
                st.success(f"Product '{new_product_name}' edited successfully!")

        if delete_button:
            # Delete product from the list
            del st.session_state.products[i]
            st.success(f"Product '{product_name}' deleted successfully!")

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

    for product in st.session_state.products:
        product_name = product["product_name"]
        qty_type = product["qty_type"]
        num_pieces = product["num_pieces"]
        price_per_piece = product["price_per_piece"]
        line_total = num_pieces * price_per_piece
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
