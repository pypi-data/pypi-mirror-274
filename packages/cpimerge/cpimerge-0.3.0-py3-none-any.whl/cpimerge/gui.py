import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from .descriptions import gui_descriptions
from .merge import run_merge
from .load import load_files
from .config import save_config

# File selection dialog
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    check_ics1_entry()

# Output file selection dialog
def select_output_file(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
    check_output_entry()

# Clear the content of the entry
def clear_entry(entry):
    entry.delete(0, tk.END)
    check_ics1_entry()
    check_output_entry()

# Show description in a new window
def show_description(key, root):
    description_window = tk.Toplevel(root)
    description_window.title("Description")
    description_window.geometry("400x300")
    description_window.resizable(False, False)
    description_window.transient(root)
    description_window.grab_set()

    # Center the new window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - 200
    y = (screen_height // 2) - 150
    description_window.geometry(f"400x300+{x}+{y}")

    frame = tk.Frame(description_window, bd=2, relief=tk.RAISED)
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text=gui_descriptions[key], wraplength=380, justify=tk.LEFT)
    label.pack(padx=10, pady=10)

    close_button = tk.Button(frame, text="Close", command=description_window.destroy)
    close_button.pack(pady=10)

# Check if ics1_entry has a value and enable/disable the checkbox accordingly
def check_ics1_entry():
    if ics1_entry.get().strip():
        rename_checkbox.config(state=tk.NORMAL)
    else:
        rename_checkbox.config(state=tk.DISABLED)
        rename_var.set(False)

def check_output_entry(*args):
    if output_entry.get().strip() and os.path.exists(output_entry.get().strip()):
        open_button.config(state=tk.NORMAL)
    else:
        open_button.config(state=tk.DISABLED)

def view_edit_exclusions_file(exclusions_entry, root):
    file_path = exclusions_entry.get().strip()
    if not file_path:
        messagebox.showwarning("Warning", "No exclusions file selected.")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read exclusions file:\n{e}")
        return

    def save_exclusions():
        try:
            with open(file_path, 'w') as file:
                file.write(text_widget.get("1.0", tk.END).strip())
            messagebox.showinfo("Success", "Exclusions file saved successfully.")
            exclusions_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save exclusions file:\n{e}")

    exclusions_window = tk.Toplevel(root)
    exclusions_window.title("Exclusions Editor")
    exclusions_window.geometry("600x600")
    exclusions_window.transient(root)
    exclusions_window.grab_set()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - 300
    y = (screen_height // 2) - 200
    exclusions_window.geometry(f"600x600+{x}+{y}")

    text_frame = tk.Frame(exclusions_window)
    text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    text_widget = tk.Text(text_frame, wrap=tk.WORD, undo=True)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.insert(tk.END, content)

    button_frame = tk.Frame(exclusions_window)
    button_frame.pack(pady=10)

    save_button = tk.Button(button_frame, text="Save", command=save_exclusions)
    save_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=exclusions_window.destroy)
    cancel_button.pack(side=tk.LEFT, padx=10)

# View file content in a new window
def view_file(entry, root):
    file_path = entry.get().strip()
    if not file_path:
        messagebox.showwarning("Warning", "No file selected.")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
        return

    file_view_window = tk.Toplevel(root)
    file_view_window.title("File Viewer")
    file_view_window.geometry("600x600")
    file_view_window.transient(root)
    file_view_window.grab_set()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - 300
    y = (screen_height // 2) - 200
    file_view_window.geometry(f"600x600+{x}+{y}")

    text_frame = tk.Frame(file_view_window)
    text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    text_widget = tk.Text(text_frame, wrap=tk.WORD)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.insert(tk.END, content)

    close_button = tk.Button(file_view_window, text="Close", command=file_view_window.destroy)
    close_button.pack(pady=10)

def save_state(config_path):
    config = {
        "ics1_path": ics1_entry.get(),
        "ics2_path": ics2_entry.get(),
        "exclusions_path": exclusions_entry.get(),
        "output_path": output_entry.get(),
        "rename_state": rename_var.get()
    }
    save_config(config, config_path)
    messagebox.showinfo("Success", "Configuration saved successfully.")

def open_output_file(file_path):
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(file_path)
        elif os.name == 'posix':
            subprocess.run(['open', file_path], check=True)  # For macOS
            # subprocess.run(['xdg-open', file_path], check=True)  # For Linux (uncomment if needed)
    except Exception as e:
        print(f"Error opening file: {e}")

def initialize_gui(config, config_path):
    global ics1_entry, ics2_entry, exclusions_entry, output_entry, rename_checkbox, rename_var, open_button

    # Initialize GUI
    root = tk.Tk()
    root.title(gui_descriptions["root_title"])

    # Calculate the position to center the window
    window_width = 1100
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # GUI elements
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Button(frame, text="?", command=lambda: show_description("ics1_description", root)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame, text="Previous iCal Export (ics1) (optional):").grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    ics1_entry = tk.Entry(frame, width=50)
    ics1_entry.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    ics1_entry.insert(0, config.get("ics1_path", ""))
    ics1_entry.bind("<KeyRelease>", lambda event: check_ics1_entry())
    tk.Button(frame, text="Clear", command=lambda: clear_entry(ics1_entry)).grid(row=0, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_file(ics1_entry)).grid(row=0, column=4, padx=10, pady=5)
    tk.Button(frame, text="View", command=lambda: view_file(ics1_entry, root)).grid(row=0, column=5, padx=10, pady=5)

    tk.Button(frame, text="?", command=lambda: show_description("ics2_description", root)).grid(row=1, column=0, padx=10, pady=5)
    tk.Label(frame, text="New iCal Export (ics2):").grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
    ics2_entry = tk.Entry(frame, width=50)
    ics2_entry.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    ics2_entry.insert(0, config.get("ics2_path", ""))
    tk.Button(frame, text="Clear", command=lambda: clear_entry(ics2_entry)).grid(row=1, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_file(ics2_entry)).grid(row=1, column=4, padx=10, pady=5)
    tk.Button(frame, text="View", command=lambda: view_file(ics2_entry, root)).grid(row=1, column=5, padx=10, pady=5)

    tk.Button(frame, text="?", command=lambda: show_description("exclusions_description", root)).grid(row=2, column=0, padx=10, pady=5)
    tk.Label(frame, text="Exclusions File (optional):").grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    exclusions_entry = tk.Entry(frame, width=50)
    exclusions_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    exclusions_entry.insert(0, config.get("exclusions_path", ""))
    tk.Button(frame, text="Clear", command=lambda: clear_entry(exclusions_entry)).grid(row=2, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_file(exclusions_entry)).grid(row=2, column=4, padx=10, pady=5)
    tk.Button(frame, text="Edit", command=lambda: view_edit_exclusions_file(exclusions_entry, root)).grid(row=2, column=5, padx=10, pady=5)

    tk.Button(frame, text="?", command=lambda: show_description("output_description", root)).grid(row=3, column=0, padx=10, pady=5)
    tk.Label(frame, text="Output File:").grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
    output_entry = tk.Entry(frame, width=50)
    output_entry.grid(row=3, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    output_entry.insert(0, config.get("output_path", ""))
    output_entry.bind("<KeyRelease>", check_output_entry)
    tk.Button(frame, text="Clear", command=lambda: clear_entry(output_entry)).grid(row=3, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_output_file(output_entry)).grid(row=3, column=4, padx=10, pady=5)
    tk.Button(frame, text="View", command=lambda: view_file(output_entry, root)).grid(row=3, column=5, padx=10, pady=5)
    
    rename_var = tk.BooleanVar(value=(config.get("rename_state", False)))
    rename_checkbox = tk.Checkbutton(frame, text="Replace ics1 with ics2 after merging (ics1 and ics2 will be backed up)", variable=rename_var)
    rename_checkbox.grid(row=4, column=0, columnspan=6, pady=5)
    rename_checkbox.config(state=tk.DISABLED)  # Initially disable the checkbox

    button_frame = tk.Frame(frame)
    button_frame.grid(row=5, column=0, columnspan=6, pady=20)

    tk.Button(button_frame, text="Load", command=lambda: load_files(ics1_entry, ics2_entry, exclusions_entry, output_text)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Merge", command=lambda: run_merge(ics1_entry, ics2_entry, exclusions_entry, output_entry, rename_var, output_text, config_path)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Save Configuration", command=lambda: save_state(config_path)).pack(side=tk.LEFT, padx=10)
    open_button = tk.Button(button_frame, text="Open Output in Defaut App", state=tk.DISABLED, command=lambda: open_output_file(output_entry.get()))
    open_button.pack(side=tk.LEFT, padx=10)

    output_frame = tk.Frame(frame)
    output_frame.grid(row=6, column=0, columnspan=6, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

    output_text = tk.Text(output_frame, height=30, width=100)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text.config(yscrollcommand=scrollbar.set)

    # Make the grid cells expand with window resizing
    frame.grid_rowconfigure(6, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    # Initial check to set the state of the checkbox
    check_ics1_entry()
    check_output_entry()

    root.mainloop()
