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
import re
import logging

from config import LOG_FILE


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataCleaner:

    def __init__(self, df):

        self.df = df.copy()

    # --------------------------------------------
    # Clean a single value
    # --------------------------------------------

    @staticmethod
    def clean_text(value):

        if pd.isna(value):
            return ""

        value = str(value)

        # Replace line breaks
        value = value.replace("\n", " ")

        # Replace tabs
        value = value.replace("\t", " ")

        # Remove extra spaces
        value = re.sub(r"\s+", " ", value)

        return value.strip()

    # --------------------------------------------
    # Clean entire dataframe
    # --------------------------------------------

    def clean_dataframe(self):

        for column in self.df.columns:

            self.df[column] = self.df[column].apply(self.clean_text)

        logging.info("Whitespace cleaned.")

    # --------------------------------------------
    # Remove blank rows
    # --------------------------------------------

    def remove_blank_rows(self):

        self.df.replace("", pd.NA, inplace=True)

        self.df.dropna(how="all", inplace=True)

        self.df.fillna("", inplace=True)

        logging.info("Blank rows removed.")

    # --------------------------------------------
    # Standardize Quantity
    # --------------------------------------------

    def clean_qty(self):

        if "Qty" not in self.df.columns:
            return

        self.df["Qty"] = (
            self.df["Qty"]
            .astype(str)
            .str.replace(",", "")
            .str.strip()
        )

        logging.info("Quantity standardized.")

    # --------------------------------------------
    # Standardize Revision
    # --------------------------------------------

    def clean_revision(self):

        if "Rev" not in self.df.columns:
            return

        self.df["Rev"] = (
            self.df["Rev"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        logging.info("Revision standardized.")

    # --------------------------------------------
    # Clean Designators
    # --------------------------------------------

    def clean_designators(self):

        if "Reference Designator" not in self.df.columns:
            return

        self.df["Reference Designator"] = (
            self.df["Reference Designator"]
            .astype(str)
            .str.replace(" ", "", regex=False)
            .str.replace(",,", ",", regex=False)
        )

        logging.info("Reference Designators cleaned.")

    # --------------------------------------------
    # Main Function
    # --------------------------------------------

    def clean(self):

        self.clean_dataframe()

        self.remove_blank_rows()

        self.clean_qty()

        self.clean_revision()

        self.clean_designators()

        logging.info("Cleaning completed.")

        return self.df


if __name__ == "__main__":

    print("Cleaner Module Loaded Successfully")