import os
import glob
import sys
import tkinter as tk
import shutil
from tkinter import filedialog, messagebox
from datetime import datetime
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
        self.root.title("RetroArch Playlist Updater by GoodLuckTrying")
        self.root.geometry("500x550")  # Window size
        self.root.configure(bg="#F0F0F0")  # Set a background color

        # Set the icon for the Tkinter window (use resource_path to get the correct icon path)
        icon_path = resource_path("Undine.ico")  # Replace with the correct icon filename
        self.root.iconbitmap(icon_path)

        # Set the initial status for the "Destination backup" check
        self.backup_var = tk.BooleanVar()
        # Set the initial folder paths to None
        self.SOURCE_folder = None
        self.DESTINATION_folder = None

        # Create the menu bar
        create_menu(self)

        # Create the UI components
        create_widgets(self)

    def check_source(self):
        source_folder = self.source_entry.get()
        
        # Check if the source folder path is not empty
        if source_folder:
            # Check if the folder exists
            if os.path.exists(source_folder):
                # Check if there are any .lpl files in the folder
                lpl_files = glob.glob(os.path.join(source_folder, "*.lpl"))
                
                if lpl_files:
                    # Folder exists and contains .lpl files, update the source entry
                    self.SOURCE_folder = source_folder
                    self.source_entry.delete(0, tk.END)  # Clear the current entry
                    self.source_entry.insert(0, self.SOURCE_folder)  # Insert the new folder path
                    self.update_file_list(self.SOURCE_folder, self.source_listbox)
                    # Change the checkmark button color to lightgreen
                    self.checkmark_button_source.config(bg="lightgreen")
                    print("Source folder is valid and contains playlists.")
                else:
                    # Folder exists but does not contain .lpl files
                    self.source_entry.delete(0, tk.END)
                    messagebox.showwarning("No Playlists", "The source folder does not contain any playlists (.lpl files).")
                    # Change the checkmark button color to gray
                    self.checkmark_button_source.config(bg="gray")
                    print("No playlists found in the source folder.")
            else:
                # Folder doesn't exist
                self.source_entry.delete(0, tk.END)
                messagebox.showerror("Folder Not Found", "The source folder does not exist.")
                # Change the checkmark button color to gray
                self.checkmark_button_source.config(bg="gray")
                print("Source folder does not exist.")
        else:
            # Source folder entry is empty
            # Change the checkmark button color to gray
            self.checkmark_button_source.config(bg="gray")
            print("Source folder entry is empty.")


    def check_destination(self):
        destination_folder = self.destination_entry.get()
        
        # Check if the source folder path is not empty
        if destination_folder:
            # Check if the folder exists
            if os.path.exists(destination_folder):
                # Check if there are any .lpl files in the folder
                lpl_files = glob.glob(os.path.join(destination_folder, "*.lpl"))
                
                if lpl_files:
                    # Folder exists and contains .lpl files, update the destination entry
                    self.DESTINATION_folder = destination_folder
                    self.destination_entry.delete(0, tk.END)  # Clear the current entry
                    self.destination_entry.insert(0, self.DESTINATION_folder)  # Insert the new folder path
                    self.update_file_list(self.DESTINATION_folder, self.destination_listbox)
                    # Change the checkmark button color to lightgreen
                    self.checkmark_button_destination.config(bg="lightgreen")
                    print("Destination folder is valid and contains playlists.")
                else:
                    # Folder exists but does not contain .lpl files
                    self.destination_entry.delete(0, tk.END)
                    messagebox.showwarning("No Playlists", "The destination folder does not contain any playlists (.lpl files).")
                    # Change the checkmark button color to gray
                    self.checkmark_button_destination.config(bg="gray")
                    print("No playlists found in the destination folder.")
            else:
                # Folder doesn't exist
                self.destination_entry.delete(0, tk.END)
                messagebox.showerror("Folder Not Found", "The destination folder does not exist.")
                # Change the checkmark button color to gray
                self.checkmark_button_destination.config(bg="gray")
                print("Destination folder does not exist.")
        else:
            # Source folder entry is empty
            # Change the checkmark button color to gray
            self.checkmark_button_destination.config(bg="gray")
            print("Destination folder entry is empty.")

    def on_source_folder_label_click(self, event):
        """Handle click on source folder label."""
        self.select_SOURCE_folder()

    def on_DESTINATION_folder_label_click(self, event):
        """Handle click on destination folder label."""
        self.select_DESTINATION_folder()

    def select_SOURCE_folder(self):
        """Open dialog to select the SOURCE folder."""
        self.SOURCE_folder = filedialog.askdirectory(title="Select the Source Folder")
        if self.SOURCE_folder:
            # Update the folder label to show the selected folder
            self.source_entry.delete(0, tk.END)  # Clear the current entry
            self.source_entry.insert(0, self.SOURCE_folder)  # Insert the new folder path
            self.update_file_list(self.SOURCE_folder, self.source_listbox)

    def select_DESTINATION_folder(self):
        """Open dialog to select the DESTINATION folder."""
        self.DESTINATION_folder = filedialog.askdirectory(title="Select the Destination Folder")
        if self.DESTINATION_folder:
            # Update the folder label to show the selected folder
            self.destination_entry.delete(0, tk.END)  # Clear the current entry
            self.destination_entry.insert(0, self.DESTINATION_folder)  # Insert the new folder path
            self.update_file_list(self.DESTINATION_folder, self.destination_listbox)

# Buttons under Source Playlists listbox
    def restart_app(self):
        """Clear paths, clear listboxes, and restarts the file lists."""
        try:
            # Clear the source and destination folder paths
            self.SOURCE_folder = ""
            self.DESTINATION_folder = ""

            # Clear the listboxes
            self.source_listbox.delete(0, tk.END)
            self.destination_listbox.delete(0, tk.END)

            # Clear the entries
            self.source_entry.delete(0, tk.END)
            self.destination_entry.delete(0, tk.END)
            # Optionally, load new default files or show a message (you can customize this)
            #self.source_listbox.insert(tk.END, "No source files loaded.")
            #self.destination_listbox.insert(tk.END, "No destination files loaded.")
            
            print("App has been restarted.")
        except Exception as e:
            print(f"Error in restart_app: {e}")

        
        self.backup_var.set(False)

    def backup_destination(self):
        # Use the DESTINATION_folder set in the app
        destination_folder = self.DESTINATION_folder  # Get folder from the class instance

        if not destination_folder:  # Check if the destination folder is set
            messagebox.showerror("Error", "Destination folder not selected!")
            return

        # Create a timestamp for the backup folder name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(destination_folder, f"backup_{timestamp}")

        # Ensure the backup folder exists
        os.makedirs(backup_folder, exist_ok=True)

        # Copy the .lpl files (or other necessary files) to the backup folder
        for file_name in os.listdir(destination_folder):
            if file_name.endswith('.lpl'):  # Adjust if necessary to other types of playlists
                source_file = os.path.join(destination_folder, file_name)
                backup_file = os.path.join(backup_folder, file_name)
                shutil.copy2(source_file, backup_file)  # Copy the file and preserve metadata

        print(f"Backup completed to {backup_folder}")

# Buttons under Destination Playlists listbox
    def select_all(self):
        """Select all items in the destination listbox."""
        try:
            self.destination_listbox.select_set(0, tk.END)    # Select all items in the destination listbox
        except Exception as e:
            print(f"Error in select_all: {e}")

    def clear_selection(self):
        """Deselect all items in the destination listbox."""
        try:
            self.destination_listbox.select_clear(0, tk.END)    # Deselect all items in destination listbox
        except Exception as e:
            print(f"Error in clear_selection: {e}")

    def execute(self):
        """Execute the process of updating the destination files."""
        selected_files = [self.destination_listbox.get(i) for i in self.destination_listbox.curselection()]
        if not selected_files:
            messagebox.showwarning("No files selected", "Please select at least one file to update.")
            return
        if self.backup_var.get():  # If checkbox is checked
            self.backup_destination()  # Perform backup
        updated_files = process_folders(self.SOURCE_folder, self.DESTINATION_folder, selected_files)
        if updated_files:
            messagebox.showinfo("Success", f"The following playlists were updated: {', '.join(updated_files)}")
        else:
            messagebox.showwarning("No updates", "No playlists were updated.")

    def exit_app(self):
        """Exit the application."""
        self.root.quit()

#Functions in gui_utils.py
    def show_about(self):
        """Show an 'About' message in a custom window with a fixed size."""
        show_about(self)

    def update_file_list(self, folder, listbox):
        """Update the file list in the listbox."""
        update_file_list(self, folder, listbox)
