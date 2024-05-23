import os
from icalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from .ical import load_ics, get_event_set, create_all_day_event
from .exclusions import load_exclusions, filter_exclusions
from .descriptions import merge_descriptions

# Main function to merge calendars
def merge(ics1_path, ics2_path, exclusions_path, excl_text, remove_text, merge_text):
    try:
        # Load the calendars from the input files
        if os.path.exists(ics1_path):
            cal1 = load_ics(ics1_path)
        else:
            merge_text.insert(tk.END, merge_descriptions["no_ical"])
            cal1 = Calendar()
        if os.path.exists(ics2_path):
            cal2 = load_ics(ics2_path)

        # Sanity check
        if cal1 is None and cal2 is None:
            merge_text.insert(tk.END, merge_descriptions["no_reach"])
            return

        # Load and the exclusions
        if not exclusions_path:
            excl_text.insert(tk.END, "No EXCL file provided.\n\n")
            exclusions = []
        else:
            exclusions = load_exclusions(exclusions_path)
            if exclusions:
                excl_text.insert(tk.END, f"Excluding any event(s) matching:\n\n")
                for excl in exclusions:
                    excl_text.insert(tk.END, f"  - '{excl}'\n")
                excl_text.insert(tk.END, "\n")
            else:
                excl_text.insert(tk.END, "EXCL file was provided, but it was empty.\n\n")

        # Create  set of events from each calendar
        events1 = get_event_set(cal1) if cal1 else set()
        events2 = get_event_set(cal2)

        # Generate unique events for each calendar
        unique_events_ics2 = events2 - events1  # These are the initial new events to be added to to the output ical
        unique_events_ics1 = events1 - events2  # These are used to report possible events to manually remove

        # Remove exclusions from the unique_events_ics2
        filtered_events = filter_exclusions(unique_events_ics2, exclusions, excl_text)

        # Create a new calendar of all-day events from the filtered_events
        output_cal = Calendar()
        for event in filtered_events:
            output_cal.add_component(create_all_day_event(event))

        #
        # TO DO: This should not include filtered events!
        #
        # If there was a ics1, report any event that exits in cal1 but not cal2 as possible removals, in sorted order
        if os.path.exists(ics1_path):
            if len(unique_events_ics1):
                remove_text.insert(tk.END, f"Consider removing the following events from your calendar.\n\nThey existed in ICS1 but are not in ICS2 and thus may no longer be relevant:\n\n")
                for event in sorted(unique_events_ics1, key=lambda x: x[1]):
                    remove_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")
            else:
                remove_text.insert(tk.END, f"No suggeted removals from the current calendar were found in ICS1.")
        else:
            remove_text.insert(tk.END, "First run detected. No removals from the current calendar are suggested.")

        # Report overall result
        if len(filtered_events) > 0:
            if os.path.exists(ics1_path):
                merge_text.insert(tk.END, f"There are {len(filtered_events)} new event(s) in ICS2 that do not exist in ICS1. These event(s) are:\n\n")
            else:
                merge_text.insert(tk.END, f"There are {len(filtered_events)} new event(s) in ICS2. These event(s) are:\n\n")
            # Print out events in sorted order
            for event in sorted(filtered_events, key=lambda x: x[1]):
                merge_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")
        else:
            merge_text.insert(tk.END, f"No new events were found in ICS2.\n")

        return output_cal

    except Exception as e:
        messagebox.showerror("Error", f"An unknown error occurred during the merge process: {e}")

# Run merge process
def run_merge(ics1_entry, ics2_entry, exclusions_entry, excl_text, remove_text, merge_text):
    ics1_path = ics1_entry.get()
    ics2_path = ics2_entry.get()
    exclusions_path = exclusions_entry.get()
    # output_path = output_entry.get()
    
    if not ics2_path:
        messagebox.showerror("Error", "ics2 field must be filled out.")
        return

    if ics1_path and not os.path.exists(ics1_path):
        messagebox.showerror("Error", f"File not found: {ics1_path}")
        return

    if not os.path.exists(ics2_path):
        messagebox.showerror("Error", f"File not found: {ics2_path}")
        return

    if exclusions_path and not os.path.exists(exclusions_path):
        messagebox.showerror("Error", f"File not found: {exclusions_path}")
        return

    return merge(ics1_path, ics2_path, exclusions_path if exclusions_path else None, excl_text, remove_text, merge_text)
