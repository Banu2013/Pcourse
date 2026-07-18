"""
=========================================================
BaavaTech BOM Automation Tool
Version : 1.0

Developed by:
BaavaTech

Author:
Banumathi

Copyright © 2026 BaavaTech.
All Rights Reserved.
=========================================================
"""

import os

from extractor.pdf_reader import PDFReader
from extractor.table_extractor import TableExtractor
from extractor.row_merger import RowMerger
from extractor.cleaner import DataCleaner
from extractor.validator import Validator

from vse.vse_generator import VSEGenerator
from vse.vse_verifier import VSEVerifier

from reports.report_generator import ReportGenerator


def run_bom_automation(pdf_file, template_file, output_folder):
    """
    Runs the complete BOM Automation process.
    """
    cleaned_file = os.path.join(output_folder, "Cleaned_BOM.xlsx")

    review_file = os.path.join(output_folder, "Review_Report.xlsx")

    generated_vse = os.path.join(output_folder, "Generated_VSE.xlsx")

    verification_file = os.path.join(output_folder, "Verification_Report.xlsx")

    final_report = os.path.join(output_folder, "Final_Report.xlsx")

    log_file = os.path.join(output_folder, "BOM_Automation.log")

    if not os.path.exists(pdf_file):
        raise FileNotFoundError(f"PDF not found:\n{pdf_file}")

    if not os.path.exists(template_file):
        raise FileNotFoundError(f"Template not found:\n{template_file}")

    os.makedirs(output_folder, exist_ok=True)

    print("=" * 60)
    print("BOM AUTOMATION STARTED")
    print("=" * 60)

    # -------------------------------------------------
    # Read PDF
    # -------------------------------------------------

    print("Reading PDF...")

    reader = PDFReader(pdf_file)
    pdf = reader.open()

    # -------------------------------------------------
    # Extract Tables
    # -------------------------------------------------

    print("Extracting tables...")

    extractor = TableExtractor(pdf)
    df = extractor.extract()

    # -------------------------------------------------
    # Merge Wrapped Rows
    # -------------------------------------------------

    print("Merging wrapped rows...")

    merger = RowMerger(df)
    df = merger.merge()

    # -------------------------------------------------
    # Clean Data
    # -------------------------------------------------

    print("Cleaning data...")

    cleaner = DataCleaner(df)
    df = cleaner.clean()

    # -------------------------------------------------
    # Save Cleaned BOM
    # -------------------------------------------------

    cleaned_file = os.path.join(
        output_folder,
        "Cleaned_BOM.xlsx"
    )

    df.to_excel(cleaned_file, index=False)

    print("Cleaned BOM saved.")

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    print("Validating BOM...")

    validator = Validator(df)

    review_df = validator.validate()

    review_file = os.path.join(
        output_folder,
        "Review_Report.xlsx"
    )

    review_df.to_excel(
        review_file,
        index=False
    )

    print("Validation completed.")

    # -------------------------------------------------
    # Generate VSE
    # -------------------------------------------------

    print("Generating VSE...")

    generator = VSEGenerator(
        cleaned_file,
        template_file,
        output_folder
    )

    generator.generate()

    # -------------------------------------------------
    # Verify VSE
    # -------------------------------------------------

    print("Verifying VSE...")

    verification_file = os.path.join(
    output_folder,
    "Verification_Report.xlsx"
)

    generated_vse = os.path.join(
    output_folder,
    "Generated_VSE.xlsx"
)

    verifier = VSEVerifier(
    cleaned_file,
    generated_vse,
    verification_file
)

    verifier.verify()

    # -------------------------------------------------
    # Final Report
    # -------------------------------------------------

    print("Generating Final Report...")

    report = ReportGenerator(output_folder)

    report.generate()

    reader.close()

    print("=" * 60)
    print("BOM AUTOMATION COMPLETED")
    print("=" * 60)

    return True