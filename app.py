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
import sys
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import run_bom_automation

class BOMAutomationGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BaavaTech BOM Automation Tool v1.0")
        self.root.geometry("850x450")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="BAAVATECH BOM AUTOMATION TOOL",
            font=("Arial", 18, "bold"),
            fg="navy"
        )
        title.pack(pady=(15, 5))

        company = tk.Label(
            self.root,
            text="Developed by Banumathi | BaavaTech",
            font=("Arial", 10, "italic"),
            fg="gray"
        )
        company.pack(pady=(0, 15))

        # Input Frame
        frm = tk.Frame(self.root)
        frm.pack(fill="x", padx=10, pady=10)

        tk.Label(frm, text="PDF").grid(row=0, column=0, sticky="w")
        self.pdf_entry = tk.Entry(frm, width=70)
        self.pdf_entry.grid(row=0, column=1)
        tk.Button(frm, text="Browse", command=self.browse_pdf).grid(row=0, column=2)

        tk.Label(frm, text="Template").grid(row=1, column=0, sticky="w")
        self.template_entry = tk.Entry(frm, width=70)
        self.template_entry.grid(row=1, column=1)
        tk.Button(frm, text="Browse", command=self.browse_template).grid(row=1, column=2)

        tk.Label(frm, text="Output").grid(row=2, column=0, sticky="w")
        self.output_entry = tk.Entry(frm, width=70)
        self.output_entry.grid(row=2, column=1)
        tk.Button(frm, text="Browse", command=self.browse_output).grid(row=2, column=2)

# -------------------------------------------------
# Run Button
# -------------------------------------------------

        run_btn = tk.Button(
            self.root,
            text="RUN AUTOMATION",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.run_automation
)
        run_btn.pack(pady=20)

# -------------------------------------------------
# Progress Bar
# -------------------------------------------------

        self.progress = ttk.Progressbar(
        self.root,
        orient="horizontal",
        length=500,
        mode="determinate"
)
        self.progress.pack(pady=10)

# -------------------------------------------------
# Status Label
# -------------------------------------------------

        self.status = tk.Label(
        self.root,
        text="Ready",
        fg="blue"
)
        self.status.pack()
    def browse_pdf(self):
        f=filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
        if f:
            self.pdf_entry.delete(0,tk.END); self.pdf_entry.insert(0,f)
    def browse_template(self):
        f=filedialog.askopenfilename(filetypes=[("Excel","*.xlsx")])
        if f:
            self.template_entry.delete(0,tk.END); self.template_entry.insert(0,f)
    def browse_output(self):
        d=filedialog.askdirectory()
        if d:
            self.output_entry.delete(0,tk.END); self.output_entry.insert(0,d)
    def update_progress(self,v,msg):
        self.progress["value"]=v
        self.status.config(text=msg)
        self.root.update_idletasks()

    def run_automation(self):

        pdf = self.pdf_entry.get().strip()
        tpl = self.template_entry.get().strip()
        out = self.output_entry.get().strip()

        print("PDF:", repr(pdf))
        print("Template:", repr(tpl))
        print("Output:", repr(out))

        if not pdf:
            messagebox.showerror("Error", "Please select a PDF file.")
        return

        if not tpl:
            messagebox.showerror("Error", "Please select a VSE Template.")
        return

        if not out:
            messagebox.showerror("Error", "Please select an Output Folder.")
        return

        try:
            self.update_progress(10, "Running...")

            run_bom_automation(pdf, tpl, out)

            self.update_progress(100, "Completed")

            messagebox.showinfo(
                "Success",
                "BOM Automation Completed Successfully!"
        )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_progress(0, "Failed")
            
if __name__ == "__main__":
    BOMAutomationGUI()        