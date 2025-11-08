from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

pdf = canvas.Canvas("test.pdf", pagesize=A4)
pdf.drawString(100, 800, "✅ Test PDF created successfully!")
pdf.save()

print("PDF bana diya gaya hai — 'test.pdf' file isi folder me milegi.")
