import tkinter as tk
from tkinter import ttk
from datetime import datetime
from bot.scanner import perform_scan  # Adjust this import if your folder structure is different

def main():
    print("Starting tender scan...")
    tenders = perform_scan()  # Run your scanner and get fresh matched tenders list

    tenders_valid = []
    for tender in tenders:
        try:
            tender["closing_date_dt"] = datetime.strptime(tender["closing_date"], "%d-%b-%Y %I:%M %p")
            tenders_valid.append(tender)
        except Exception as e:
            print(f"Skipping tender (bad closing date): {tender} | Error: {e}")

    tenders_sorted = sorted(tenders_valid, key=lambda x: x["closing_date_dt"])

    for tender in tenders_sorted:
        del tender["closing_date_dt"]

    root = tk.Tk()
    root.title("Tender List")
    root.geometry("900x400")

    columns = ("Reference No", "Title", "Closing Date")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=300)

    tree.pack(fill=tk.BOTH, expand=True)

    for tender in tenders_sorted:
        tree.insert("", "end", values=(
            tender.get("tender_id", "N/A"),
            tender.get("title", "N/A"),
            tender.get("closing_date", "N/A")
        ))

    root.mainloop()

if __name__ == "__main__":
    main()
