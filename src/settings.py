import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PATH_TEMPLATE_DOCX = os.path.join(BASE_DIR, "assets/templates/order.docx")