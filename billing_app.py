import streamlit as st
import datetime
from fpdf import FPDF

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

# --- PDF generation class ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Om Guru Store', ln=True, align='C')
        self.ln(5)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Date: {datetime.date.today().strftime("%d-%m-%Y")}', ln=True, align='C')
        self.ln(10)

    def bill_table(self, bill_items, total):
        self.set_font('Arial', 'B', 12)
        self.cell(70, 10, 'Product', 1)
        self.cell(30, 10, 'Qty', 1, align='C')
        self.cell(40, 10, 'Unit Price', 1, align='C')
        self.cell(40, 10, 'Total', 1, ln=True, align='C')

        self.set_font('Arial', '', 12)
        for product, (qty, price, line_total) in bill_items.items():
            self.cell(70, 10, product, 1)
            self.cell(30, 10, str(qty), 1, align='C')
            self.cell(40, 10, f"{price:.2f}", 1, align='C')
            self.cell(40, 10, f"{line_total:.2f}", 1, ln=True, align='C')

        self.set_font('Arial', 'B', 12)
        self.cell(140, 10, 'Total', 1)
        self.cell(40, 10, f"{total:.2f}", 1, ln=True, align='C')

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

    # --- PDF Creation ---
    pdf = PDF()
    pdf.add_page()
    pdf.bill_table(bill_items, total)

    pdf_output = pdf.output(dest='S').encode('latin-1')

    st.download_button(
        label="Download Bill as PDF",
        data=pdf_output,
        file_name="bill.pdf",
        mime="application/pdf"
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

    # Suggestion for Android users: They can choose contact after link opens
    st.info("📱 Tip: After clicking the link, you can choose the contact from your WhatsApp app.")

