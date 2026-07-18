"""
=========================================================
BaavaTech BOM Automation Tool
Version : 1.0
=========================================================
"""

import os
import pdfplumber


class PDFReader:
    """
    Opens and validates the BOM PDF.
    """

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf = None

    def validate(self):
        """
        Check whether the PDF exists.
        """

        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(
                f"PDF file not found:\n{self.pdf_path}"
            )

        if not self.pdf_path.lower().endswith(".pdf"):
            raise ValueError("Selected file is not a PDF.")

    def open(self):
        """
        Open the PDF.
        """

        self.validate()

        try:
            self.pdf = pdfplumber.open(self.pdf_path)
            return self.pdf

        except Exception as e:
            raise Exception(f"Unable to open PDF:\n{e}")

    def page_count(self):
        """
        Return number of pages.
        """

        if self.pdf is None:
            self.open()

        return len(self.pdf.pages)

    def close(self):
        """
        Close the PDF.
        """

        if self.pdf is not None:
            self.pdf.close()
            self.pdf = None


if __name__ == "__main__":

    pdf_file = r"Input\03-445726-00_REV_A_VSE_01_BOM_DC.pdf"

    reader = PDFReader(pdf_file)

    pdf = reader.open()

    print("--------------------------------")
    print("PDF opened successfully")
    print("Pages :", reader.page_count())
    print("--------------------------------")

    reader.close()