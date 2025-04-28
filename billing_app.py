import streamlit as st
import datetime
from io import BytesIO
from fpdf import FPDF

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
    qty = st.number_input(f"{product} - Quantity", min_value=0, step=1, key=f"{product}_qty")
    price = st.number_input(f"{product} - Price per unit", min_value=0.0, step=0.5, key=f"{product}_price")
    if qty > 0 and price > 0:
        bill_items[product] = (qty, price)

# Function to create PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Om Guru Store', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f"Date: {datetime.date.today().strftime('%d-%m-%Y')}", 0, 1, 'C')
        self.ln(5)

    def bill_table(self, items, total):
        self.set_font('Arial', 'B', 10)
        self.cell(60, 10, 'Product', 1)
        self.cell(30, 10, 'Qty', 1)
        self.cell(40, 10, 'Unit Price', 1)
        self.cell(40, 10, 'Total Price', 1)
        self.ln()

        self.set_font('Arial', '', 10)
        for product, (qty, price) in items.items():
            self.cell(60, 10, product, 1)
            self.cell(30, 10, str(qty), 1)
            self.cell(40, 10, f"{price:.2f}", 1)
            self.cell(40, 10, f"{qty * price:.2f}", 1)
            self.ln()

        self.set_font('Arial', 'B', 12)
        self.cell(130, 10, 'Total', 1)
        self.cell(40, 10, f"{total:.2f}", 1)
        self.ln()

# Generate bill
if st.button("Generate Bill"):
    st.subheader("🧾 Bill:")

    total = 0
    for product, (qty, price) in bill_items.items():
        total += qty * price

    # Text version for display
    bill_text = []
    bill_text.append(f"------ Om Guru Store ------")
    bill_text.append(f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    bill_text.append("-" * 50)
    bill_text.append(f"{'Product':20} {'Qty':>5} {'Unit':>8} {'Total':>10}")
    bill_text.append("-" * 50)
    for product, (qty, price) in bill_items.items():
        line_total = qty * price
        bill_text.append(f"{product:20} {qty:5} {price:8.2f} {line_total:10.2f}")
    bill_text.append("-" * 50)
    bill_text.append(f"{'Total':35} {total:10.2f}")
    bill_text.append("-" * 50)

    bill_result = "\n".join(bill_text)
    st.text(bill_result)

    # PDF generation
    pdf = PDF()
    pdf.add_page()
    pdf.bill_table(bill_items, total)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="Download Bill as PDF",
        data=pdf_buffer,
        file_name="bill.pdf",
        mime="application/pdf"
    )

    # Sharing on Mobile
    st.markdown("### 📱 Share Bill")
    import urllib.parse
    share_text = urllib.parse.quote(bill_result)

    share_url = f"https://api.whatsapp.com/send?text={share_text}"

    st.markdown(
        f'<a href="{share_url}" target="_blank"><button style="background-color:green;color:white;padding:10px 20px;border:none;border-radius:5px;">Share via Mobile</button></a>',
        unsafe_allow_html=True
    )
