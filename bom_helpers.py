"""
=========================================================
BOM Helper Functions
Project : BOM Automation Tool
Author  : Banumathi
=========================================================
"""

import re


# --------------------------------------------------------
# Safe String
# --------------------------------------------------------

def safe_string(value):
    """Convert any value to a clean string."""

    if value is None:
        return ""

    return str(value).strip()


# --------------------------------------------------------
# Normalize Text
# --------------------------------------------------------

def normalize_text(value):
    """Remove extra spaces and compare without case."""

    return safe_string(value).upper()


# --------------------------------------------------------
# Normalize Revision
# --------------------------------------------------------

def normalize_revision(value):
    """
    Converts:
    1
    1.0
    1.000

    into

    1
    """

    value = safe_string(value)

    if value == "":
        return ""

    try:
        number = float(value)

        if number.is_integer():
            return str(int(number))

        return str(number)

    except:
        return value.upper()


# --------------------------------------------------------
# Normalize Quantity
# --------------------------------------------------------

def normalize_quantity(value):

    value = safe_string(value)

    if value == "":
        return ""

    try:
        qty = float(value)

        if qty.is_integer():
            return str(int(qty))

        return str(qty)

    except:
        return value


# --------------------------------------------------------
# Split Alternate Manufacturer Part Numbers
# --------------------------------------------------------

def split_mpn(value):

    value = normalize_text(value)

    if value == "":
        return []

    value = value.replace(",", ";")

    return [
        part.strip()
        for part in value.split(";")
        if part.strip()
    ]


# --------------------------------------------------------
# Compare Manufacturer Part Numbers
# --------------------------------------------------------

def compare_mpn(source, generated):

    generated = normalize_text(generated)

    alternates = split_mpn(source)

    return generated in alternates


# --------------------------------------------------------
# Clean Reference Designator
# --------------------------------------------------------

def clean_designator(value):

    value = normalize_text(value)

    value = value.replace(" ", "")

    value = value.replace("\n", "")

    return value


# --------------------------------------------------------
# Safe Compare
# --------------------------------------------------------

def compare_values(source, target):

    return normalize_text(source) == normalize_text(target)