import os
import tkinter as tk
from icalendar import Calendar
from tkinter import messagebox
from .ical import load_ics, get_event_set
from .exclusions import load_exclusions

# Function to set text color in the text widget
def insert_text_with_color(text_widget, text, color):
    text_widget.tag_configure(color, foreground=color)
    text_widget.insert(tk.END, text, color)

# Load files and display information
def load_files(ics1_entry, ics2_entry, exclusions_entry, ics_text, excl_text):
    ics1_path = ics1_entry.get()
    ics2_path = ics2_entry.get()
    exclusions_path = exclusions_entry.get()

    if ics1_path and not os.path.exists(ics1_path):
        messagebox.showerror("Error", f"File not found (ICS1): {ics1_path}")
        return
    
    if not ics2_path:
        messagebox.showerror("Error", "ICS2 file must be provided")
        return

    if not os.path.exists(ics2_path):
        messagebox.showerror("Error", f"File not found (ICS2): {ics2_path}")
        return

    if exclusions_path and not os.path.exists(exclusions_path):
        messagebox.showerror("Error", f"File not found (exclusion): {exclusions_path}")
        return

    if ics1_path:
        cal1 = load_ics(ics1_path)
    else:
        ics_text.insert(tk.END, f"No ICS1 provided. Using an empty iCal.\n")
        cal1 = Calendar()
    
    cal2 = load_ics(ics2_path)
    if cal2 is None:
        return

    events1 = get_event_set(cal1) if cal1 else set()
    events2 = get_event_set(cal2)

    earliest_event_ics1 = (min(events1, key=lambda x: x[1])[1]).date() if events1 else None
    latest_event_ics1 = (max(events1, key=lambda x: x[1])[1]).date() if events1 else None
    earliest_event_ics2 = (min(events2, key=lambda x: x[1])[1]).date() if events2 else None
    latest_event_ics2 = (max(events2, key=lambda x: x[1])[1]).date() if events2 else None

    if ics1_path:
        ics_text.insert(tk.END, f"ICS1 contains {len(events1)} events:\n\n")
        if earliest_event_ics1 and latest_event_ics1:
            ics_text.insert(tk.END, f"  - Earliest event in ICS1: {earliest_event_ics1}\n")
            ics_text.insert(tk.END, f"  - Latest event in ICS1: {latest_event_ics1}\n")

    if cal2:
        ics_text.insert(tk.END, f"\nICS2 contains {len(events2)} events:\n\n")
        if earliest_event_ics2 and latest_event_ics2:
            ics_text.insert(tk.END, f"  - Earliest event in ICS2: {earliest_event_ics2}\n")
            ics_text.insert(tk.END, f"  - Latest event in ICS2: {latest_event_ics2}\n")

        if earliest_event_ics2 and earliest_event_ics1 and earliest_event_ics2 < earliest_event_ics1:
            insert_text_with_color(ics_text, "\nWarning: ICS2 has events before the earliest event in ICS1\n", "Red")
        if latest_event_ics2 and latest_event_ics1 and latest_event_ics1 > latest_event_ics2:
            insert_text_with_color(ics_text, "\nWarning: ICS1 has events after the latest event in ICS2\n", "Red")

    # Load the exclusions
    exclusions = load_exclusions(exclusions_path) if exclusions_path else []
    if not exclusions_path:
        excl_text.insert(tk.END, "No EXCL file provided.\n\n")
        exclusions = []
    else:
        exclusions = load_exclusions(exclusions_path)
        if exclusions:
            excl_text.insert(tk.END, f"EXCL contains {len(exclusions)} exclusions:\n\n")
            for excl in exclusions:
                excl_text.insert(tk.END, f"  - '{excl}'\n")
        else:
                excl_text.insert(tk.END, "EXCL file was provided, but it was empty.\n\n")