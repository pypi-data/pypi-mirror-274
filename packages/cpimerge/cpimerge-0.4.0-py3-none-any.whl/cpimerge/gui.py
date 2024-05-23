import os
import subprocess
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from .descriptions import gui_descriptions
from .merge import run_merge
from .load import load_files
from .config import save_config, get_outdir

# File selection dialog (ICS1, ICS2, EXCL)
def select_file(entry, root):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    # check_ics1_entry()
    root.update_idletasks()
    root.lift()
    root.focus_force()
    root.attributes('-topmost', 1)
    root.attributes('-topmost', 0)
    validate_files()

# Clear the content of the entry
def clear_entry(entry):
    entry.delete(0, tk.END)
    # check_ics1_entry()
    # check_output_entry()
    validate_files()

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

# Validate ICS1, ICS1, and EXCL entries and update UI states
def validate_files():
    ics1_valid = os.path.isfile(ics1_entry.get().strip())
    ics2_valid = os.path.isfile(ics2_entry.get().strip())
    exclusions_valid = os.path.isfile(exclusions_entry.get().strip())
    # output_valid = os.path.isfile(output_entry.get().strip())
    
    ics1_view_button.config(state=tk.NORMAL if ics1_valid else tk.DISABLED)
    ics2_view_button.config(state=tk.NORMAL if ics2_valid else tk.DISABLED)
    exclusions_edit_button.config(state=tk.NORMAL if exclusions_valid else tk.DISABLED)
    analyze_button.config(state=tk.NORMAL if ics2_valid else tk.DISABLED)
    merge_button.config(state=tk.NORMAL if ics2_valid else tk.DISABLED)

# Window to view and edit the EXCL file
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

    # Disable root window when active
    exclusions_window.transient(root)
    exclusions_window.grab_set()

    # Calculate the position to center the window
    window_width = 600
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    exclusions_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

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
    cancel_button = tk.Button(button_frame, text="Cancel", command=exclusions_window.destroy) # Consider changing to use on_window_close
    cancel_button.pack(side=tk.LEFT, padx=10)

# Window to view the ICS files
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

    # Disable root window when active
    file_view_window.transient(root)
    file_view_window.grab_set()

    # Calculate the position to center the window
    window_width = 600
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    file_view_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    text_frame = tk.Frame(file_view_window)
    text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    text_widget = tk.Text(text_frame, wrap=tk.WORD)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.insert(tk.END, content)

    close_button = tk.Button(file_view_window, text="Close", command=file_view_window.destroy) # Consider changing to use on_window_close
    close_button.pack(pady=10)

# Save UI selections to configuration file
def save_state(config_path):
    config = {
        "ics1_path": ics1_entry.get(),
        "ics2_path": ics2_entry.get(),
        "exclusions_path": exclusions_entry.get(),
        # "output_path": output_entry.get(),
    }
    save_config(config, config_path)
    messagebox.showinfo("Success", "Configuration saved successfully.")

# Open the OUT file in the default application
def open_output_file(file_path):
    try:
        if platform.system() == 'Windows':
            os.startfile(file_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(['open', file_path])
        elif platform.system() == 'Linux':
            subprocess.call(['xdg-open', file_path])
        else:
            messagebox.showerror("Unsupported OS", "Your operating system is not supported for this operation.")
    except Exception as e:
        print(f"Error opening file: {e}")

# Restore root focus on sub-window close
def on_window_close(window, root):
    window.grab_release()
    window.destroy()
    root.focus_force()

# Analyze window
def analyze_button_action(ics1_entry, ics2_entry, exclusions_entry, root):
    analyze_window = tk.Toplevel()
    analyze_window.title("Analyze Results")
    analyze_window.resizable(True, True)
    
    # Disable root window when active
    analyze_window.transient(root)
    analyze_window.grab_set()

    # Calculate the position to center the window
    window_width = 800
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    analyze_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    frame = tk.Frame(analyze_window)
    frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Configure grid weights to ensure equal resizing
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    def create_text_widget(parent):
        container = tk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        text_widget = tk.Text(container, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(container, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return text_widget

    ics_text = create_text_widget(left_frame)
    exl_text = create_text_widget(right_frame)

    close_button = tk.Button(analyze_window, text="Close", command=lambda: on_window_close(analyze_window, root))
    close_button.pack(pady=10)

    analyze_window.protocol("WM_DELETE_WINDOW", lambda: on_window_close(analyze_window, root))

    load_files(ics1_entry, ics2_entry, exclusions_entry, ics_text, exl_text)

# Merge window
def merge_button_action(ics1_entry, ics2_entry, exclusions_entry, root):
    icalresults = ""

    merge_window = tk.Toplevel()
    merge_window.title("Merge Results")
    merge_window.resizable(True, True)

    # Disable root window when active
    merge_window.transient(root)
    merge_window.grab_set()

    # Calculate the position to center the window
    window_width = 1500
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    merge_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    frame = tk.Frame(merge_window)
    frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    left_frame.grid(row=0, column=0, sticky="nsew")

    middle_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    middle_frame.grid(row=0, column=1, sticky="nsew")

    right_frame = tk.Frame(frame, bd=2, relief=tk.SUNKEN)
    right_frame.grid(row=0, column=2, sticky="nsew")

    # Configure grid weights to ensure equal resizing
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    def create_text_widget(parent):
        container = tk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        text_widget = tk.Text(container, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(container, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return text_widget

    excl_text = create_text_widget(left_frame)
    remove_text = create_text_widget(middle_frame)
    merge_text = create_text_widget(right_frame)

    def save_suggested_removals():
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile="Removals.txt")
        try:
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(remove_text.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("Error", f"An unknown error occurred during saving: {e}")

    def save_merge_results():
        save_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")], initialfile="Output.ics")
        try:
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(icalresults.to_ical())
                messagebox.showinfo("Success", "ICS file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An unknown error occurred during saving: {e}")

    def open_merge_results():
        save_path = get_outdir()
        try:
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(icalresults.to_ical())
            open_output_file(save_path)
        except Exception as e:
            messagebox.showerror("Error", f"An unknown error occurred during opening: {e}")

    save_suggested_button = tk.Button(frame, text="Save Suggested Removals", command=save_suggested_removals)
    save_suggested_button.grid(row=1, column=1, pady=5, padx=5)

    button_frame = tk.Frame(frame)
    button_frame.grid(row=1, column=2, pady=5, padx=5)

    save_merge_button = tk.Button(button_frame, text="Save Events to .ics", command=save_merge_results)
    save_merge_button.pack(side=tk.LEFT, padx=5)

    open_merge_button = tk.Button(button_frame, text="Import Events to Calendar", command=open_merge_results)
    open_merge_button.pack(side=tk.LEFT, padx=5)

    # Centering the buttons in the middle and right frames
    middle_frame.grid_rowconfigure(1, weight=1)
    middle_frame.grid_columnconfigure(0, weight=1)
    save_suggested_button.grid(sticky="")

    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid(sticky="")

    close_button = tk.Button(merge_window, text="Close", command=lambda: on_window_close(merge_window, root))
    close_button.pack(pady=10)

    merge_window.protocol("WM_DELETE_WINDOW", lambda: on_window_close(merge_window, root))

    # Call the merge function and direct the output to the text widgets
    icalresults = run_merge(ics1_entry, ics2_entry, exclusions_entry, excl_text, remove_text, merge_text)

# Main/root UI window
def initialize_gui(config, config_path):
    global ics1_entry, ics2_entry, exclusions_entry, ics1_view_button, ics2_view_button, exclusions_edit_button, analyze_button, merge_button
    
    # Initialize GUI
    root = tk.Tk()
    root.title(gui_descriptions["root_title"])

    # Calculate the position to center the window
    window_width = 1100
    window_height = 190
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # GUI elements
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    # ICS1
    tk.Button(frame, text="?", command=lambda: show_description("ics1_description", root)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame, text=gui_descriptions["ics1"]).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    ics1_entry = tk.Entry(frame, width=50)
    ics1_entry.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    ics1_entry.insert(0, config.get("ics1_path", ""))
    tk.Button(frame, text="Clear", command=lambda: clear_entry(ics1_entry)).grid(row=0, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_file(ics1_entry, root)).grid(row=0, column=4, padx=10, pady=5)
    ics1_view_button = tk.Button(frame, text="View", command=lambda: view_file(ics1_entry, root), state=tk.DISABLED)
    ics1_view_button.grid(row=0, column=5, padx=10, pady=5)
    ics1_entry.bind("<KeyRelease>", lambda event: validate_files())
    
    # ICS2
    tk.Button(frame, text="?", command=lambda: show_description("ics2_description", root)).grid(row=1, column=0, padx=10, pady=5)
    tk.Label(frame, text=gui_descriptions["ics2"]).grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
    ics2_entry = tk.Entry(frame, width=50)
    ics2_entry.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    ics2_entry.insert(0, config.get("ics2_path", ""))
    tk.Button(frame, text="Clear", command=lambda: clear_entry(ics2_entry)).grid(row=1, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_file(ics2_entry, root)).grid(row=1, column=4, padx=10, pady=5)
    ics2_view_button = tk.Button(frame, text="View", command=lambda: view_file(ics2_entry, root), state=tk.DISABLED)
    ics2_view_button.grid(row=1, column=5, padx=10, pady=5)
    ics2_entry.bind("<KeyRelease>", lambda event: validate_files())

    # EXCL
    tk.Button(frame, text="?", command=lambda: show_description("exclusions_description", root)).grid(row=2, column=0, padx=10, pady=5)
    tk.Label(frame, text=gui_descriptions["exclusion"]).grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    exclusions_entry = tk.Entry(frame, width=50)
    exclusions_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W+tk.E)
    exclusions_entry.insert(0, config.get("exclusions_path", ""))
    tk.Button(frame, text="Clear", command=lambda: clear_entry(exclusions_entry)).grid(row=2, column=3, padx=10, pady=5)
    tk.Button(frame, text="Browse", command=lambda: select_file(exclusions_entry, root)).grid(row=2, column=4, padx=10, pady=5)
    exclusions_edit_button = tk.Button(frame, text="Edit", command=lambda: view_edit_exclusions_file(exclusions_entry, root), state=tk.DISABLED)
    exclusions_edit_button.grid(row=2, column=5, padx=10, pady=5)
    exclusions_entry.bind("<KeyRelease>", lambda event: validate_files())

    # Button frame for holding the bottom buttons
    button_frame = tk.Frame(frame)
    button_frame.grid(row=3, column=0, columnspan=6, pady=20)
    # Analyze button
    analyze_button = tk.Button(button_frame, text="Analyze", state=tk.DISABLED, command=lambda: analyze_button_action(ics1_entry, ics2_entry, exclusions_entry, root))
    analyze_button.pack(side=tk.LEFT, padx=10)
    # Merge button
    merge_button = tk.Button(button_frame, text="Merge", state=tk.DISABLED, command=lambda: merge_button_action(ics1_entry, ics2_entry, exclusions_entry, root))
    merge_button.pack(side=tk.LEFT, padx=10)
    # Save button
    tk.Button(button_frame, text="Save Configuration", command=lambda: save_state(config_path)).pack(side=tk.LEFT, padx=10)
    
    # Make the grid cells expand with window resizing
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    # File validity checks
    validate_files()

    root.mainloop()
