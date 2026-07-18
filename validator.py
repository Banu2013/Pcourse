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
import logging
import re

from config import (
    LOG_FILE,
    MANDATORY_COLUMNS,
    DUPLICATE_COLUMNS,
    NUMERIC_COLUMNS
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Validator:

    def __init__(self, df):

        self.df = df.copy()

        self.errors = []

        self.allowed_uom = [
            "EA",
            "PCS",
            "SET",
            "KIT",
            "M",
            "MM",
            "CM",
            "IN",
            "FT"
        ]

    #######################################################
    # Add Error
    #######################################################

    def add_error(
        self,
        row,
        column,
        error,
        value="",
        severity="Critical",
        suggestion=""
    ):

        self.errors.append({

            "Row": row + 2,

            "Item #":
                self.df.at[row, "Item #"]
                if "Item #" in self.df.columns else "",

            "Lvl":
                self.df.at[row, "Lvl"]
                if "Lvl" in self.df.columns else "",

            "VSE P/N":
                self.df.at[row, "VSE P/N"]
                if "VSE P/N" in self.df.columns else "",

            "Customer P/N":
                self.df.at[row, "Customer P/N"]
                if "Customer P/N" in self.df.columns else "",

            "Column": column,

            "Value": value,

            "Error": error,

            "Severity": severity,

            "Suggestion": suggestion

        })

    #######################################################
    # Mandatory Fields
    #######################################################

    def check_mandatory(self):

        logging.info("Checking Mandatory Fields...")

        for column in MANDATORY_COLUMNS:

            if column not in self.df.columns:
                continue

            for idx, value in self.df[column].items():

                if pd.isna(value) or str(value).strip() == "":

                    self.add_error(

                        idx,

                        column,

                        "Missing Mandatory Field",

                        "",

                        "Critical",

                        f"Populate '{column}'"

                    )

    #######################################################
    # Duplicate Values
    #######################################################

    def check_duplicates(self):

        logging.info("Checking Duplicate Values...")

        for column in DUPLICATE_COLUMNS:

            if column not in self.df.columns:
                continue

            duplicate_rows = self.df[
                self.df[column].duplicated(keep=False)
            ]

            for idx in duplicate_rows.index:

                value = self.df.at[idx, column]

                if str(value).strip() == "":
                    continue

                self.add_error(

                    idx,

                    column,

                    "Duplicate Value",

                    value,

                    "Critical",

                    "Remove duplicate"

                )

    #######################################################
    # Numeric Validation
    #######################################################

    def check_numeric(self):

        logging.info("Checking Numeric Columns...")

        for column in NUMERIC_COLUMNS:

            if column not in self.df.columns:
                continue

            for idx, value in self.df[column].items():

                if str(value).strip() == "":
                    continue

                try:

                    float(value)

                except:

                    self.add_error(

                        idx,

                        column,

                        "Invalid Numeric",

                        value,

                        "Critical",

                        "Enter valid number"

                    )

    #######################################################
    # Revision Validation
    #######################################################

    def check_revision(self):

        if "Rev" not in self.df.columns:
            return

        logging.info("Checking Revision...")

        pattern = r"^[A-Za-z0-9.\-_]+$"

        for idx, value in self.df["Rev"].items():

            value = str(value).strip()

            if value == "":
                continue

            if not re.match(pattern, value):

                self.add_error(

                    idx,

                    "Rev",

                    "Invalid Revision",

                    value,

                    "Warning",

                    "Verify revision"

                )

    #######################################################
    # UOM Validation
    #######################################################

    def check_uom(self):

        if "UOM" not in self.df.columns:
            return

        logging.info("Checking UOM...")

        for idx, value in self.df["UOM"].items():

            value = str(value).upper().strip()

            if value == "":
                continue

            if value not in self.allowed_uom:

                self.add_error(

                    idx,

                    "UOM",

                    "Invalid UOM",

                    value,

                    "Warning",

                    "Verify UOM"

                )

    #######################################################
    # Blank Rows
    #######################################################

    def check_blank_rows(self):

        logging.info("Checking Blank Rows...")

        for idx in self.df.index:

            row = self.df.loc[idx]

            if all(str(x).strip() == "" for x in row):

                self.add_error(

                    idx,

                    "",

                    "Blank Row",

                    "",

                    "Warning",

                    "Remove blank row"

                )

    #######################################################
    # Run Validation
    #######################################################

    def validate(self):

        logging.info("Validation Started")

        self.check_mandatory()

        self.check_duplicates()

        self.check_numeric()

        self.check_revision()

        self.check_uom()

        self.check_blank_rows()

        review_df = pd.DataFrame(self.errors)

        logging.info(f"Validation Completed ({len(review_df)} Errors)")

        return review_df


###########################################################
# Test
###########################################################

if __name__ == "__main__":

    print("Validator Module Loaded Successfully")