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

from config import LOG_FILE

# ---------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------

logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
)


class RowMerger:

    def __init__(self, df):

        self.df = df.copy()

        self.rows_to_delete = []

    # -----------------------------------------------------
    # Clean Text
    # -----------------------------------------------------

    @staticmethod
    def clean(value):

        if pd.isna(value):
            return ""

        return str(value).strip()

    # -----------------------------------------------------
    # Merge Description / Manufacturer
    # -----------------------------------------------------

    def merge_with_space(self, old_text, new_text):

        old_text = self.clean(old_text)
        new_text = self.clean(new_text)

        if old_text == "":
            return new_text

        if new_text == "":
            return old_text

        if new_text in old_text:
            return old_text

        return old_text + " " + new_text

    # -----------------------------------------------------
    # Merge Designator / Manufacturer PN
    # -----------------------------------------------------

    def merge_without_space(self, old_text, new_text):

        old_text = self.clean(old_text)
        new_text = self.clean(new_text)

        if old_text == "":
            return new_text

        if new_text == "":
            return old_text

        if new_text in old_text:
            return old_text

        return old_text + new_text

    # -----------------------------------------------------
    # Fill if Blank
    # -----------------------------------------------------

    def fill_if_blank(self, old_text, new_text):

        old_text = self.clean(old_text)
        new_text = self.clean(new_text)

        if old_text == "":
            return new_text

        return old_text

    # -----------------------------------------------------
    # Check Continuation Row
    # -----------------------------------------------------

    def is_continuation_row(self, row):

        key_columns = [
            "Lvl",
            "Level",
             "Item #",
             "Item",
             "Qty",
             "Quantity",
             "VSE P/N",
             "VSE Part Number"
    ]

        for column in key_columns:

            if column in self.df.columns:

                value = self.clean(row.get(column))

            if value != "":
                return False

            return True

    # -----------------------------------------------------
    # Merge Row
    # -----------------------------------------------------

    def merge_row(self, previous_index, current_index):

        # Description
        if "Description" in self.df.columns:
            self.df.at[previous_index, "Description"] = self.merge_with_space(
                self.df.at[previous_index, "Description"],
                self.df.at[current_index, "Description"]
            )

        # Reference Designator
        if "Reference Designator" in self.df.columns:
            self.df.at[previous_index, "Reference Designator"] = self.merge_without_space(
                self.df.at[previous_index, "Reference Designator"],
                self.df.at[current_index, "Reference Designator"]
            )

        # Manufacturer
        if "Manufacturer" in self.df.columns:
            self.df.at[previous_index, "Manufacturer"] = self.merge_with_space(
                self.df.at[previous_index, "Manufacturer"],
                self.df.at[current_index, "Manufacturer"]
            )

        # Manufacturer P/N
        if "Manufacturer P/N" in self.df.columns:
            self.df.at[previous_index, "Manufacturer P/N"] = self.merge_without_space(
                self.df.at[previous_index, "Manufacturer P/N"],
                self.df.at[current_index, "Manufacturer P/N"]
            )

        # Customer P/N
        if "Customer P/N" in self.df.columns:
            self.df.at[previous_index, "Customer P/N"] = self.fill_if_blank(
                self.df.at[previous_index, "Customer P/N"],
                self.df.at[current_index, "Customer P/N"]
            )

        # UOM
        if "UOM" in self.df.columns:
            self.df.at[previous_index, "UOM"] = self.fill_if_blank(
                self.df.at[previous_index, "UOM"],
                self.df.at[current_index, "UOM"]
            )

        # Revision
        if "Rev" in self.df.columns:
            self.df.at[previous_index, "Rev"] = self.fill_if_blank(
                self.df.at[previous_index, "Rev"],
                self.df.at[current_index, "Rev"]
            )

        self.rows_to_delete.append(current_index)

        logging.info(
            f"Merged Row {current_index} into Row {previous_index}"
        )

    # -----------------------------------------------------
    # Main Merge
    # -----------------------------------------------------

    def merge(self):

        previous_index = None

        for current_index in self.df.index:

            row = self.df.loc[current_index]

            if self.is_continuation_row(row):

                if previous_index is not None:
                    self.merge_row(previous_index, current_index)

            else:
                previous_index = current_index

        if self.rows_to_delete:

            self.df.drop(
                index=self.rows_to_delete,
                inplace=True
            )

            self.df.reset_index(
                drop=True,
                inplace=True
            )

        logging.info(
            f"Removed {len(self.rows_to_delete)} continuation rows."
        )

        return self.df


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    print("Row Merger Loaded Successfully")