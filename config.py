"""
=========================================================
BaavaTech BOM Automation Tool
Version : 2.0

Developed by:
BaavaTech

Author:
Banumathi

Copyright © 2026 BaavaTech.
All Rights Reserved.
=========================================================
"""

import os

# =========================================================
# Project Information
# =========================================================

APP_NAME = "BaavaTech BOM Automation Tool"
VERSION = "2.0.0"

# =========================================================
# Project Paths
# =========================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(PROJECT_ROOT, "Input")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "Output")
LOG_FOLDER = os.path.join(PROJECT_ROOT, "Logs")
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "Templates")

for folder in [INPUT_FOLDER, OUTPUT_FOLDER, LOG_FOLDER, TEMPLATE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# =========================================================
# Files
# =========================================================

LOG_FILE = os.path.join(LOG_FOLDER, "BOM_Automation.log")

VSE_TEMPLATE = os.path.join(
    TEMPLATE_FOLDER,
    "VSE_Template.xlsx"
)

# =========================================================
# Output Files
# =========================================================

EXTRACTED_BOM = os.path.join(
    OUTPUT_FOLDER,
    "Extracted_BOM.xlsx"
)

MERGED_BOM = os.path.join(
    OUTPUT_FOLDER,
    "Merged_BOM.xlsx"
)

CLEANED_BOM = os.path.join(
    OUTPUT_FOLDER,
    "Cleaned_BOM.xlsx"
)

GENERATED_VSE = os.path.join(
    OUTPUT_FOLDER,
    "Generated_VSE.xlsx"
)

VERIFICATION_REPORT = os.path.join(
    OUTPUT_FOLDER,
    "Verification_Report.xlsx"
)

FINAL_REPORT = os.path.join(
    OUTPUT_FOLDER,
    "Final_Report.xlsx"
)

# =========================================================
# VSE Template Settings
# =========================================================

VSE_SHEET = "VSE_BOM"

HEADER_ROW = 8

DATA_START_ROW = 9

# =========================================================
# Mandatory Columns
# =========================================================

MANDATORY_COLUMNS = [
    "Lvl",
    "Item #",
    "VSE P/N",
    "Qty",
    "Customer P/N",
    "Rev",
    "Description",
    "Reference Designator",
    "UOM",
    "Manufacturer",
    "Manufacturer P/N"
]

# =========================================================
# Duplicate Validation
# =========================================================

DUPLICATE_COLUMNS = [
    "Item #",
    "VSE P/N",
    "Customer P/N",
    "Reference Designator"
]

# =========================================================
# Numeric Validation
# =========================================================

NUMERIC_COLUMNS = [
    "Lvl",
    "Qty"
]

# =========================================================
# Header Detection
# =========================================================

HEADER_KEYWORDS = [
    "Lvl",
    "Item #",
    "Qty",
    "Description",
    "Customer P/N",
    "VSE P/N",
    "Manufacturer",
    "Manufacturer P/N",
    "Reference Designator",
    "Rev",
    "UOM"
]

# =========================================================
# Ignore Footer Text
# =========================================================

IGNORE_FOOTERS = [
    "Commodity Codes",
    "Confidential",
    "Assembly Number",
    "Printed",
    "Page",
    "RoHS"
]

# =========================================================
# Allowed UOM
# =========================================================

ALLOWED_UOM = [
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

print("BaavaTech BOM Automation Tool Configuration Loaded")