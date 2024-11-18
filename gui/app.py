import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_handler import process_folders
from gui.gui_utils import create_menu, create_widgets, show_about, update_file_list

def resource_path(relative_path):
    """Get the absolute path to a resource in the bundled executable."""
    try:
        # For a frozen app (when running as an exe)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # This is the temporary folder where PyInstaller extracts the files
        else:
            base_path = os.path.abspath(".")  # If running from source code
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting resource path: {e}")
        return relative_path  # Fallback to the relative path if something goes wrong

class PlaylistUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RetroArch Playlist Updater & Synchronizer by GoodLuckTrying")
        self.root.geometry("700x500")
        self.root.configure(bg="#F0F0F0")

        # Set the icon for the Tkinter window (use resource_path to get the correct icon path)
        icon_path = resource_path("Undine.ico")  # Replace with the correct icon filename
        self.root.iconbitmap(icon_path)

        # Set the initial folder paths to None
        self.source_folder = None
        self.DESTINATION_folder = None

        # Create the menu bar
        create_menu(self)

        # Create the UI components
        create_widgets(self)

    def exit_app(self):
        """Exit the application."""
        self.root.quit()

    def on_source_folder_label_click(self, event):
        """Handle click on source folder label."""
        self.select_source_folder()

    def on_DESTINATION_folder_label_click(self, event):
        """Handle click on destination folder label."""
        self.select_DESTINATION_folder()

    def refresh_app(self):
        """Reset the app's folder selections and lists."""
        self.source_folder = None
        self.DESTINATION_folder = None
        
        self.source_folder_label.config(text="No source folder selected")
        self.DESTINATION_folder_label.config(text="No destination folder selected")
        
        self.source_listbox.delete(0, tk.END)
        self.DESTINATION_listbox.delete(0, tk.END)

    def select_source_folder(self):
        """Open dialog to select the SOURCE folder."""
        self.source_folder = filedialog.askdirectory(title="Select the Source Folder")
        if self.source_folder:
            self.source_folder_label.config(text=f"Source Folder: {self.source_folder}")
            self.update_file_list(self.source_folder, self.source_listbox)

    def select_DESTINATION_folder(self):
        """Open dialog to select the DESTINATION folder."""
        self.DESTINATION_folder = filedialog.askdirectory(title="Select the Destination Folder")
        if self.DESTINATION_folder:
            self.DESTINATION_folder_label.config(text=f"Destination Folder: {self.DESTINATION_folder}")
            self.update_file_list(self.DESTINATION_folder, self.DESTINATION_listbox)

    def update_file_list(self, folder, listbox):
        """Update the file list in the listbox."""
        update_file_list(self, folder, listbox)

    def select_all(self):
        """Select all items in the Destination listbox."""
        for index in range(self.DESTINATION_listbox.size()):
            self.DESTINATION_listbox.select_set(index)

    def clear_selection(self):
        """Clear all selections in the Destination listbox."""
        self.DESTINATION_listbox.selection_clear(0, tk.END)

    def execute(self):
        """Execute the process of updating the destination files."""
        selected_files = [self.DESTINATION_listbox.get(i) for i in self.DESTINATION_listbox.curselection()]
        if not selected_files:
            messagebox.showwarning("No files selected", "Please select at least one file to update.")
            return

        updated_files = process_folders(self.source_folder, self.DESTINATION_folder, selected_files)
        if updated_files:
            messagebox.showinfo("Success", f"The following playlists were updated: {', '.join(updated_files)}")
        else:
            messagebox.showwarning("No updates", "No playlists were updated.")

    def show_about(self):
        """Show an 'About' message in a custom window with a fixed size."""
        show_about(self)