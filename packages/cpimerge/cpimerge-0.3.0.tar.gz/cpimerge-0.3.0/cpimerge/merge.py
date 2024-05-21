import os
from icalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from .ical import load_ics, get_event_set, create_all_day_event
from .config import save_config
from .exclusions import load_exclusions, filter_exclusions
from .backup import backup_file

# Main function to merge calendars
def merge(ics1_path, ics2_path, exclusions_path, output_path, output_text, rename_ics2):
    try:
        # Load the calendars from the input files
        if os.path.exists(ics1_path):
            cal1 = load_ics(ics1_path)
        else:
            output_text.insert(tk.END, f"No ics1 provided. Using an empty iCal.\n")
            cal1 = Calendar()
        if os.path.exists(ics2_path):
            cal2 = load_ics(ics2_path)

        # Sanity check
        if cal1 is None and cal2 is None:
            output_text.insert(tk.END, "This shouldn't be reached: cal1 and cal2 are empty.\n")
            return

        # Load and process the exclusions, if any
        exclusions = load_exclusions(exclusions_path) if exclusions_path else []
        if exclusions:
            output_text.insert(tk.END, f"\nExclusions from '{exclusions_path}':\n")
            for excl in exclusions:
                output_text.insert(tk.END, f"  - '{excl}'\n")
            output_text.insert(tk.END, "\n")

        # Create  set of events from each calendar
        events1 = get_event_set(cal1) if cal1 else set()
        events2 = get_event_set(cal2)

        # Generate unique events for each calendar
        unique_events_ics2 = events2 - events1  # These are the initial new events to be added to to the output ical
        unique_events_ics1 = events1 - events2  # These are used to report possible events to manually remove

        # Remove exclusions from the unique_events_ics2
        filtered_events = filter_exclusions(unique_events_ics2, exclusions, output_text)

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
                output_text.insert(tk.END, f"Consider removing the following events from your calendar. They existed in '{ics1_path}' but are not in '{ics2_path}' and thus may no longer be relevant:\n")
                for event in sorted(unique_events_ics1, key=lambda x: x[1]):
                    output_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")
            else:
                output_text.insert(tk.END, f"No suggeted removals from the current calendar were found in '{ics1_path}'.\n")
        else:
            output_text.insert(tk.END, "First run detected. No removals from the current calendar are suggested.\n")

        # Report overall result
        if len(filtered_events) > 0:
            if os.path.exists(ics1_path):
                output_text.insert(tk.END, f"\nThere are {len(filtered_events)} new event(s) in:\n\t'{ics2_path}'\nThat do not exist in: '{ics1_path}'\nThese event(s) will be output to:\n\t'{output_path}'\nThese event(s) are:\n")
            else:
                output_text.insert(tk.END, f"\nThere are {len(filtered_events)} new event(s) in:\n\t'{ics2_path}'\nThey will be output to:\n\t'{output_path}'\nThese event(s) are:\n")
            # Print out events in sorted order
            for event in sorted(filtered_events, key=lambda x: x[1]):
                output_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")
            # Write the new calendar to the output_path
            with open(output_path, 'wb') as f:
                f.write(output_cal.to_ical())
        else:
            output_text.insert(tk.END, f"\nNo new events were found in:\n\t'{ics2_path}'\n")

        # If the rename option was chosen, do the backups and the rename
        if rename_ics2:
            if os.path.exists(ics1_path):
                backup_ics1_path = backup_file(ics1_path)
                output_text.insert(tk.END, f"\nBackup of '{ics1_path}' created: {backup_ics1_path}\n")
            if os.path.exists(ics2_path):
                backup_ics2_path = backup_file(ics2_path)
                output_text.insert(tk.END, f"\nBackup of '{ics2_path}' created: {backup_ics2_path}\n")   
            os.remove(ics1_path)
            os.rename(ics2_path, ics1_path)
            output_text.insert(tk.END, f"\nRenamed {ics2_path} to {ics1_path} for use for the next run.\n")

    except Exception as e:
        messagebox.showerror("Error", f"An unknown error occurred during the merge process: {e}")

# Run merge process
def run_merge(ics1_entry, ics2_entry, exclusions_entry, output_entry, rename_var, output_text, config_path):
    ics1_path = ics1_entry.get()
    ics2_path = ics2_entry.get()
    exclusions_path = exclusions_entry.get()
    output_path = output_entry.get()
    rename_ics2 = rename_var.get()

    if not all([ics2_path, output_path]):
        messagebox.showerror("Error", "ics2 and output file fields must be filled out")
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

    output_text.delete(1.0, tk.END)
    merge(ics1_path, ics2_path, exclusions_path if exclusions_path else None, output_path, output_text, rename_ics2)
    output_text.insert(tk.END, f"\nCalendars merged successfully.\n\n** You can now import the new events from {output_path} **")