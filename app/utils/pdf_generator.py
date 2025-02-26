from fpdf import FPDF

def generate_invoice(order_id, user, items, total_price):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="QuitQ Order Invoice", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Order ID: {order_id}", ln=True)
    pdf.cell(200, 10, txt=f"Customer: {user.name} ({user.email})", ln=True)

    for item in items:
        pdf.cell(200, 10, txt=f"{item.product.name} x {item.quantity} - ${item.product.price * item.quantity}", ln=True)

    pdf.cell(200, 10, txt=f"Total: ${total_price}", ln=True)
    pdf.output(f"invoice_{order_id}.pdf")

    return f"invoice_{order_id}.pdf"
