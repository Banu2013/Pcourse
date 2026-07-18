"""
=========================================================
Progress Manager
Project : BOM Automation Tool
Author  : Banumathi
=========================================================
"""


class ProgressManager:

    def __init__(self):
        self.percent = 0
        self.message = "Starting..."

    def update(self, percent, message):

        self.percent = percent
        self.message = message

        print(f"[{percent}%] {message}")

    def get_progress(self):
        return self.percent, self.message