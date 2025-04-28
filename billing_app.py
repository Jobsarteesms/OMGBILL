import streamlit as st
import datetime

# Initial products
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

st.title("🛒 Om Guru Store - Billing App")
st.write(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")

# Option to add new products
new_product = st.text_input("Add a new product (optional):")
if new_product:
    products.append(new_product)

st.header("Enter Product Details:")

bill_items = {}
for product in products:
    qty = st.number_input(f"{product} - Quantity", min_value=0, step=1)
    price = st.number_input(f"{product} - Price per unit", min_value=0.0, step=0.5)
    if qty > 0 and price > 0:
        bill_items[product] = (qty, price)

# Generate bill
if st.button("Generate Bill"):
    st.subheader("🧾 Bill:")
    total = 0
    bill_text = []
    bill_text.append(f"------ Om Guru Store ------")
    bill_text.append(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    bill_text.append("-" * 30)
    bill_text.append(f"{'Product':20} {'Qty':>5} {'Price':>10}")
    bill_text.append("-" * 30)
    for product, (qty, price) in bill_items.items():
        line_total = qty * price
        bill_text.append(f"{product:20} {qty:5} {line_total:10.2f}")
        total += line_total
    bill_text.append("-" * 30)
    bill_text.append(f"{'Total':25} {total:10.2f}")
    bill_text.append("-" * 30)

    bill_result = "\n".join(bill_text)
    st.text(bill_result)

    st.download_button("Download Bill", bill_result, file_name="bill.txt")

    # WhatsApp Sharing Link
    st.markdown("### Share on WhatsApp")
    message = bill_result.replace('\n', '%0A')  # format for WhatsApp
    phone_number = st.text_input("Enter WhatsApp Number (with country code, e.g., +91...)")
    if st.button("Share via WhatsApp"):
        if phone_number:
            whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={message}"
            st.markdown(f"[Click here to share]( {whatsapp_url} )", unsafe_allow_html=True)
        else:
            st.error("Please enter a phone number")

    # Email sharing can be added using external services too

