import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import webbrowser
import os

# ===================== STATE ===================== #

LIVERIES = []
results = []
livery_folder = ""

# ===================== UI ===================== #

root = tk.Tk()
root.title("LevelUp 737 Livery Manager")
root.geometry("1000x600")

top = tk.Frame(root)
top.pack(fill="x", padx=10, pady=5)

search_entry = tk.Entry(top, width=30)
search_entry.pack(side="left", padx=5)
search_entry.insert(0, "Search airline (e.g. united)")

site_var = tk.StringVar(value="All")
ttk.Combobox(
    top,
    values=["All", "iniBuilds", "Threshold"],
    textvariable=site_var,
    width=12,
    state="readonly"
).pack(side="left", padx=5)

v600 = tk.BooleanVar()
v700 = tk.BooleanVar()
v800 = tk.BooleanVar()
v900 = tk.BooleanVar()

for txt, var in [("600", v600), ("700", v700), ("800", v800), ("900", v900)]:
    tk.Checkbutton(top, text=txt, variable=var).pack(side="left")

tk.Button(top, text="Search", command=lambda: search()).pack(side="left", padx=5)
tk.Button(top, text="Import Liveries File", command=lambda: import_liveries()).pack(side="left", padx=5)

listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=10, pady=5)

bottom = tk.Frame(root)
bottom.pack(fill="x", padx=10, pady=5)

tk.Button(bottom, text="Select Livery Folder", command=lambda: select_folder()).pack(side="left")
tk.Button(bottom, text="Open Livery in Browser", command=lambda: open_livery()).pack(side="left", padx=10)
tk.Button(bottom, text="Install ZIP", command=lambda: install_zip()).pack(side="right")

status_var = tk.StringVar(value="Ready")
tk.Label(root, textvariable=status_var, anchor="w").pack(fill="x", padx=10)

# ===================== FUNCTIONS ===================== #

def import_liveries():
    global LIVERIES
    path = filedialog.askopenfilename(
        title="Select livery database file",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
    )
    if not path:
        return

    LIVERIES.clear()

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                site, variant, name, url = line.split(",", 3)
                LIVERIES.append({
                    "site": site.strip(),
                    "variant": variant.strip(),
                    "name": name.strip(),
                    "airline": name.lower(),
                    "url": url.strip()
                })

        status_var.set(f"Loaded {len(LIVERIES)} liveries")

    except Exception as e:
        messagebox.showerror("Import Error", str(e))

def select_folder():
    global livery_folder
    livery_folder = filedialog.askdirectory(title="Select LevelUp 737 liveries folder")
    if livery_folder:
        status_var.set(f"Livery folder set")

def selected_variants():
    v = []
    if v600.get(): v.append("600")
    if v700.get(): v.append("700")
    if v800.get(): v.append("800")
    if v900.get(): v.append("900")
    return v

def search():
    listbox.delete(0, tk.END)
    results.clear()

    query = search_entry.get().strip().lower()
    if query.startswith("search") or query == "":
        query = None

    variants = selected_variants()
    site_filter = site_var.get()

    for l in LIVERIES:
        if site_filter != "All" and l["site"] != site_filter:
            continue
        if query and query not in l["airline"]:
            continue
        if variants and l["variant"] not in variants:
            continue

        display = f"[{l['site']}] [-{l['variant']}] {l['name']}"
        listbox.insert(tk.END, display)
        results.append(l)

    status_var.set(f"{len(results)} liveries found")

def open_livery():
    sel = listbox.curselection()
    if not sel:
        return
    webbrowser.open(results[sel[0]]["url"])

def install_zip():
    if not livery_folder:
        messagebox.showerror("No Folder", "Select your livery folder first.")
        return

    zip_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    if not zip_path:
        return

    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(livery_folder)
        messagebox.showinfo("Success", "Livery installed successfully.")
    except Exception as e:
        messagebox.showerror("Install Error", str(e))

# ===================== START ===================== #

root.mainloop()
