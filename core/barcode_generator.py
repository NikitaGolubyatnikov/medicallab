import os
import random
import string
from datetime import datetime
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64

def generate_barcode_data(order_id: int) -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    rand_part = ''.join(random.choices(string.digits, k=6))
    return f"{order_id}{date_part}{rand_part}"

def draw_barcode(code: str, filename: str):
    width = 400
    height = 100
    background = (255, 255, 255)
    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)

    x = 10
    for char in code:
        if char.isdigit():
            digit = int(char)
            if digit == 0:
                x += 1.35
            else:
                bar_width = 0.15 * digit * 10
                draw.rectangle([x, 10, x + bar_width, 80], fill=(0, 0, 0))
                x += bar_width
            x += 2

    image.save(filename)

def generate_pdf_report_for_order(order_id: int, patient_data: dict, services: list) -> tuple[str, str]:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "barcodes"))
    os.makedirs(base_dir, exist_ok=True)

    code = generate_barcode_data(order_id)
    barcode_path = os.path.join(base_dir, f"{code}.png")
    pdf_path = os.path.join(base_dir, f"order_report_{order_id}.pdf")

    draw_barcode(code, barcode_path)

    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("DejaVu", 14)
    width, height = A4
    y = height - 50

    c.drawString(50, y, f"Отчёт по заказу #{order_id}")
    y -= 25
    c.setFont("DejaVu", 12)
    c.drawString(50, y, f"Пациент: {patient_data.get('full_name', '—')}")
    y -= 20
    c.drawString(50, y, f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    c.setFont("DejaVu", 11)
    c.drawString(50, y, "Услуга")
    c.drawString(250, y, "Код")
    c.drawString(350, y, "Результат")
    y -= 20

    for service in services:
        name = service.get("name", "—")
        code = service.get("code", "—")
        value = service.get("value", "—")
        c.drawString(50, y, str(name))
        c.drawString(250, y, str(code))
        c.drawString(350, y, str(value))
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("DejaVu", 11)

    y -= 30
    c.setFont("DejaVu", 12)
    c.drawString(50, y, "Штрих-код:")
    y -= 110
    c.drawImage(ImageReader(barcode_path), 50, y, width=200, height=60)

    c.save()

    with open(pdf_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    if os.path.exists(barcode_path):
        os.remove(barcode_path)

    return pdf_path, b64

if __name__ == "__main__":
    from bd.database import Database
    db = Database()
    order_id = 40
    order = db.get_order_by_id(order_id)
    patient = db.get_patient_by_id(order["patient_id"])
    services = db.get_order_services(order_id)
    for s in services:
        s["name"] = "Анализ крови"
        s["code"] = s.get("service_id", "–")
        s["value"] = "13.4"

    path, b64 = generate_pdf_report_for_order(order_id, patient, services)
    print("PDF path:", path)
