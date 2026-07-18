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
import logging
import pandas as pd

from config import (
   
    OUTPUT_FOLDER,
    LOG_FILE
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class VSEVerifier:

    def __init__(self, cleaned_file, generated_vse, verification_file):

        self.cleaned_file = cleaned_file
        self.generated_vse = generated_vse
        self.verification_file = verification_file

        self.source_df = None
        self.vse_df = None
        self.results = []

    # Source BOM Column -> VSE Column
        self.compare_fields = {
        "VSE P/N": "VSE Item",
        "Qty": "Qty",
        "Description": "Description",
        "Rev": "Rev",
        "UOM": "UOM",
        "Manufacturer": "Manufacturer",
        "Manufacturer P/N": "Manufacturer P/N",
        "Reference Designator": "Reference Designator"
    }
    # --------------------------------------------------
    # Load Files
    # --------------------------------------------------

    def load_files(self):

        logging.info("Loading BOM files...")

        self.source_df = pd.read_excel(self.cleaned_file)

        self.vse_df = pd.read_excel(
            self.generated_vse,
            sheet_name="VSE_BOM",
            header=7      # Excel Row 8
        )

        # Remove blank rows
        self.source_df = self.source_df.dropna(how="all")
        self.vse_df = self.vse_df.dropna(how="all")

        logging.info(
            f"Source Rows : {len(self.source_df)}"
        )

        logging.info(
            f"VSE Rows : {len(self.vse_df)}"
        )

        # --------------------------------------------------
    # Compare Source BOM with Generated VSE
    # --------------------------------------------------

    def compare_rows(self):

        logging.info("Starting VSE Verification...")

        # Remove spaces from column names
        self.source_df.columns = self.source_df.columns.str.strip()
        self.vse_df.columns = self.vse_df.columns.str.strip()

        # Check Customer P/N exists
        if "Customer P/N" not in self.source_df.columns:
            raise Exception("Customer P/N column missing in self.cleaned_file.xlsx")

        if "Cust Item" not in self.vse_df.columns:
            raise Exception("Cust Item column missing in Generated_VSE.xlsx")

        # Compare every source row
        for _, source_row in self.source_df.iterrows():

            customer_pn = str(source_row["Customer P/N"]).strip()

            # Find matching VSE row
            vse_match = self.vse_df[
                self.vse_df["Cust Item"].astype(str).str.strip() == customer_pn
            ]

            if vse_match.empty:

                self.results.append({
                    "Customer P/N": customer_pn,
                    "Field": "Customer P/N",
                    "Status": "FAIL",
                    "Remarks": "Part Missing in Generated VSE"
                })

                continue

            vse_row = vse_match.iloc[0]

            # Compare fields
            for source_col, vse_col in self.compare_fields.items():

                source_value = str(source_row.get(source_col, "")).strip()
                vse_value = str(vse_row.get(vse_col, "")).strip()

                # Ignore case
                source_compare = source_value.upper()
                vse_compare = vse_value.upper()

                # Alternate Manufacturer P/N check
                if source_col == "Manufacturer P/N":

                    alternates = [
                        x.strip().upper()
                        for x in source_compare.replace(",", ";").split(";")
                        if x.strip()
                    ]

                    if vse_compare in alternates:

                        status = "PASS"
                        remarks = "Alternate Manufacturer P/N Matched"

                    else:

                        status = "FAIL"
                        remarks = "Manufacturer P/N Mismatch"

                else:

                    if source_compare == vse_compare:

                        status = "PASS"
                        remarks = "Matched"

                    else:

                        status = "FAIL"
                        remarks = f"{source_col} Mismatch"

                self.results.append({

                    "Customer P/N": customer_pn,
                    "Field": source_col,
                    "Source": source_value,
                    "Generated VSE": vse_value,
                    "Status": status,
                    "Remarks": remarks

                })

        logging.info("Verification Completed.")

    #--------------------------------------------------
    # Save Verification Report
    # --------------------------------------------------

    def save_report(self):

        logging.info("Saving Verification Report...")

        report_df = pd.DataFrame(self.results)

        report_file = os.path.join(
            OUTPUT_FOLDER,
            "Verification_Report.xlsx"
        )

        with pd.ExcelWriter(report_file, engine="openpyxl") as writer:

            # Detailed Results
            report_df.to_excel(
                writer,
                sheet_name="Verification",
                index=False
            )

            # Summary
            total = len(report_df)
            passed = len(report_df[report_df["Status"] == "PASS"])
            failed = len(report_df[report_df["Status"] == "FAIL"])

            summary = pd.DataFrame({
                "Metric": [
                    "Total Checks",
                    "Passed",
                    "Failed"
                ],
                "Value": [
                    total,
                    passed,
                    failed
                ]
            })

            summary.to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

        logging.info(f"Verification Report Saved: {report_file}")

        print(f"\nVerification Report Created:\n{report_file}")

    # --------------------------------------------------
    # Run Verifier
    # --------------------------------------------------

    def verify(self):

        self.load_files()

        self.compare_rows()

        self.save_report()