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

import pandas as pd


class TableExtractor:

    def __init__(self, pdf):
        self.pdf = pdf

        # Expected BOM headers
        self.expected_headers = [
            "Lvl",
            "Level",
            "Item",
            "Item #",
            "Qty",
            "Quantity",
            "Description",
            "Customer",
            "Customer P/N",
            "VSE P/N",
            "Manufacturer",
            "Manufacturer P/N",
            "Reference",
            "Reference Designator",
            "Rev",
            "UOM"
        ]

    # --------------------------------------------------
    # Find Header Row
    # --------------------------------------------------

    def find_header(self, table):

        for row_index, row in enumerate(table):

            cleaned_row = [
                str(cell).replace("\n", " ").strip()
                if cell else ""
                for cell in row
            ]

            match_count = 0

            for cell in cleaned_row:

                for header in self.expected_headers:

                    if header.lower() in cell.lower():
                        match_count += 1

            # At least 3 matching headers indicates BOM header
            if match_count >= 3:
                return row_index

        return None

    # --------------------------------------------------
    # Extract Tables
    # --------------------------------------------------

    def extract(self):

        all_tables = []

        print("\nReading PDF...")

        total_pages = len(self.pdf.pages)

        for page_number, page in enumerate(self.pdf.pages, start=1):

            print(f"Reading Page {page_number}/{total_pages}")

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                if not table:
                    continue

                header_row = self.find_header(table)

                if header_row is None:
                    continue

                header = table[header_row]
                rows = table[header_row + 1:]

                if len(rows) == 0:
                    continue

                # Clean Header
                header = [
                    str(col).replace("\n", " ").strip()
                    if col else f"Column_{i}"
                    for i, col in enumerate(header)
                ]

                cleaned_rows = []

                for row in rows:

                    cleaned_rows.append([
                        str(cell).replace("\n", " ").strip()
                        if cell else ""
                        for cell in row
                    ])

                try:
                    df = pd.DataFrame(cleaned_rows, columns=header)

                except Exception:
                    continue

                # Remove completely empty rows
                df.replace("", pd.NA, inplace=True)
                df.dropna(how="all", inplace=True)

                # Remove empty columns
                df.dropna(axis=1, how="all", inplace=True)

                # Remove duplicate columns
                df = df.loc[:, ~df.columns.duplicated()]

                # Add page number
                df["PDF Page"] = page_number

                all_tables.append(df)

        if not all_tables:
            raise Exception("No BOM table found in PDF.")

        final_df = pd.concat(all_tables, ignore_index=True)

        final_df.reset_index(drop=True, inplace=True)

        print("\n===================================")
        print("PDF Extraction Completed")
        print("===================================")
        print(f"Pages Read      : {total_pages}")
        print(f"Rows Extracted  : {len(final_df)}")
        print(f"Columns Found   : {len(final_df.columns)}")
        print("===================================\n")

        return final_df