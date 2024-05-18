import tkinter as tk
from tkinter import filedialog
from .descriptions import descriptions
from .merge import run_merge
from .load import load_files

# File selection dialog
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    check_ics1_entry()

# Output file selection dialog
def select_output_file(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Show description in a new window
def show_description(key, root):
    description_window = tk.Toplevel(root)
    # description_window.title("Description")
    description_window.geometry("400x300")
    description_window.resizable(False, False)
    description_window.transient(root)
    description_window.grab_set()

    # Center the new window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - 200  # 400/2 for half the width
    y = (screen_height // 2) - 150  # 300/2 for half the height
    description_window.geometry(f"400x300+{x}+{y}")

    frame = tk.Frame(description_window, bd=2, relief=tk.RAISED)
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text=descriptions[key], wraplength=380, justify=tk.LEFT)
    label.pack(padx=10, pady=10)

    close_button = tk.Button(frame, text="Close", command=description_window.destroy)
    close_button.pack(pady=10)

# Check if ics1_entry has a value and enable/disable the checkbox accordingly
def check_ics1_entry():
    if ics1_entry.get().strip():
        rename_checkbox.config(state=tk.NORMAL)
        # rename_var.set(True)
    else:
        rename_checkbox.config(state=tk.DISABLED)
        rename_var.set(False)

# Create GUI
def initialize_gui(config, config_path):
    global ics1_entry, rename_checkbox, rename_var

    # Initialize GUI
    root = tk.Tk()
    root.title("CPI iCal Merger")

    # Calculate the position to center the window
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # GUI elements
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Previous iCal Export (ics1) (optional):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    ics1_entry = tk.Entry(frame, width=50)
    ics1_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
    ics1_entry.insert(0, config.get("ics1_path", ""))
    ics1_entry.bind("<KeyRelease>", lambda event: check_ics1_entry())
    tk.Button(frame, text="Browse", command=lambda: select_file(ics1_entry)).grid(row=0, column=2, padx=10, pady=5)
    tk.Button(frame, text="?", command=lambda: show_description("ics1_description", root)).grid(row=0, column=3, padx=10, pady=5)

    tk.Label(frame, text="New iCal Export (ics2):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    ics2_entry = tk.Entry(frame, width=50)
    ics2_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
    ics2_entry.insert(0, config.get("ics2_path", ""))
    tk.Button(frame, text="Browse", command=lambda: select_file(ics2_entry)).grid(row=1, column=2, padx=10, pady=5)
    tk.Button(frame, text="?", command=lambda: show_description("ics2_description", root)).grid(row=1, column=3, padx=10, pady=5)

    tk.Label(frame, text="Exclusions File (optional):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    exclusions_entry = tk.Entry(frame, width=50)
    exclusions_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
    exclusions_entry.insert(0, config.get("exclusions_path", ""))
    tk.Button(frame, text="Browse", command=lambda: select_file(exclusions_entry)).grid(row=2, column=2, padx=10, pady=5)
    tk.Button(frame, text="?", command=lambda: show_description("exclusions_description", root)).grid(row=2, column=3, padx=10, pady=5)

    tk.Label(frame, text="Output File:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    output_entry = tk.Entry(frame, width=50)
    output_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
    output_entry.insert(0, config.get("output_path", ""))
    tk.Button(frame, text="Browse", command=lambda: select_output_file(output_entry)).grid(row=3, column=2, padx=10, pady=5)
    tk.Button(frame, text="?", command=lambda: show_description("output_description", root)).grid(row=3, column=3, padx=10, pady=5)

    rename_var = tk.BooleanVar(value=False)
    rename_checkbox = tk.Checkbutton(frame, text="Replace ics1 with ics2 after merging (ics1 and ics2 will be backed up)", variable=rename_var)
    rename_checkbox.grid(row=4, column=0, columnspan=4, pady=5)
    rename_checkbox.config(state=tk.DISABLED)  # Initially disable the checkbox

    button_frame = tk.Frame(frame)
    button_frame.grid(row=5, column=0, columnspan=4, pady=20)

    tk.Button(button_frame, text="Load", command=lambda: load_files(ics1_entry, ics2_entry, exclusions_entry, output_text)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Merge", command=lambda: run_merge(ics1_entry, ics2_entry, exclusions_entry, output_entry, rename_var, output_text, config_path)).pack(side=tk.LEFT, padx=10)

    output_frame = tk.Frame(frame)
    output_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

    output_text = tk.Text(output_frame, height=30, width=100)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text.config(yscrollcommand=scrollbar.set)

    # Make the grid cells expand with window resizing
    frame.grid_rowconfigure(6, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Initial check to set the state of the checkbox
    check_ics1_entry()

    root.mainloop()
