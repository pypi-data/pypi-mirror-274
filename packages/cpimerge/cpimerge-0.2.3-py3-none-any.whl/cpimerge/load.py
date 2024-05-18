import os
import tkinter as tk
from icalendar import Calendar
from tkinter import messagebox
from .ical import load_ics, get_event_set
from .exclusions import load_exclusions

# Function to set text color in the output_text widget
def insert_text_with_color(text_widget, text, color):
    text_widget.tag_configure(color, foreground=color)
    text_widget.insert(tk.END, text, color)

# Load files and display information
def load_files(ics1_entry, ics2_entry, exclusions_entry, output_text):
    ics1_path = ics1_entry.get()
    ics2_path = ics2_entry.get()
    exclusions_path = exclusions_entry.get()

    if ics1_path and not os.path.exists(ics1_path):
        messagebox.showerror("Error", f"File not found (ics1): {ics1_path}")
        return
    
    if not ics2_path:
        messagebox.showerror("Error", "ics2 file must be provided")
        return

    if not os.path.exists(ics2_path):
        messagebox.showerror("Error", f"File not found (ics2): {ics2_path}")
        return

    if exclusions_path and not os.path.exists(exclusions_path):
        messagebox.showerror("Error", f"File not found (exclusion): {exclusions_path}")
        return

    output_text.delete(1.0, tk.END)

    if ics1_path:
        cal1 = load_ics(ics1_path)
    else:
        output_text.insert(tk.END, f"No ics1 provided. Using an empty iCal.\n")
        cal1 = Calendar()
    cal2 = load_ics(ics2_path)
    exclusions = load_exclusions(exclusions_path) if exclusions_path else []

    if cal2 is None:
        return

    events1 = get_event_set(cal1) if cal1 else set()
    events2 = get_event_set(cal2)

    earliest_event_ics1 = (min(events1, key=lambda x: x[1])[1]).date() if events1 else None
    latest_event_ics1 = (max(events1, key=lambda x: x[1])[1]).date() if events1 else None
    earliest_event_ics2 = (min(events2, key=lambda x: x[1])[1]).date() if events2 else None
    latest_event_ics2 = (max(events2, key=lambda x: x[1])[1]).date() if events2 else None

    output_text.insert(tk.END, f"ics1: {len(events1)} events\n")
    if earliest_event_ics1 and latest_event_ics1:
        output_text.insert(tk.END, f"Earliest event in ics1: {earliest_event_ics1}\n")
        output_text.insert(tk.END, f"Latest event in ics1: {latest_event_ics1}\n")

    if cal2:
        output_text.insert(tk.END, f"\nics2: {len(events2)} events\n")
        if earliest_event_ics2 and latest_event_ics2:
            output_text.insert(tk.END, f"Earliest event in ics2: {earliest_event_ics2}\n")
            output_text.insert(tk.END, f"Latest event in ics2: {latest_event_ics2}\n")

        if earliest_event_ics2 and earliest_event_ics1 and earliest_event_ics2 < earliest_event_ics1:
            insert_text_with_color(output_text, "Warning: ics2 has events before the earliest event in ics1\n", "Red")
        if latest_event_ics2 and latest_event_ics1 and latest_event_ics1 > latest_event_ics2:
            insert_text_with_color(output_text, "Warning: ics1 has events after the latest event in ics2\n", "Red")

    if exclusions:
        output_text.insert(tk.END, f"\nExclusions:\n")
        for excl in exclusions:
            output_text.insert(tk.END, f"  - '{excl}'\n")