# auth/captcha.py

import random
import string
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptchaGenerator:
    def __init__(self):
        self.last_text = ""

    def generate(self) -> bytes:
        width, height = 200, 60
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)

        image = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(image)

        captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        self.last_text = captcha_text

        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), captcha_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2

        draw.text((text_x, text_y), captcha_text, fill=text_color, font=font)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        logger.info(f"✅ CAPTCHA сгенерирована: {captcha_text}")
        return buffer.read()

    def get_last_text(self) -> str:
        return self.last_text
