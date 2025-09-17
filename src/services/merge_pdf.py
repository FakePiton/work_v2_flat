from PyPDF2 import PdfMerger
import os

class MergePDF:
    def __init__(self):
        self.text_info = ""

    def merge_report(self, dir_pdf: str):
        name_file = "merge_report.pdf"
        output_path = os.path.join(dir_pdf, name_file)

        merger = PdfMerger()

        for filename in sorted(os.listdir(dir_pdf)):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(dir_pdf, filename)
                merger.append(full_path)
                self.text_info += f"✅ Файл {filename} успішно об’єднано.\n"
        merger.write(output_path)
        self.text_info += f"✅ Файл [{name_file}] створено!!!"
        merger.close()
