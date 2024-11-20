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
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting resource path: {e}")
        return relative_path

class PlaylistUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RetroArch Playlist Updater 1.2 by GoodLuckTrying")
        self.root.geometry("500x550")
        self.root.configure(bg="#F0F0F0")

        icon_path = resource_path("Undine.ico")
        self.root.iconbitmap(icon_path)

        self.backup_var = tk.BooleanVar()
        self.SOURCE_folder = None
        self.DESTINATION_folder = None

        create_menu(self)
        create_widgets(self)

    def check_folder(self, folder_entry, listbox, checkmark_button, folder_type):
        """Helper function to check if a folder exists and contains .lpl files."""
        folder = folder_entry.get()

        if folder:
            if os.path.exists(folder):
                lpl_files = glob.glob(os.path.join(folder, "*.lpl"))
                if lpl_files:
                    # Update UI for valid folder
                    self.update_folder(folder, folder_entry, listbox, checkmark_button, folder_type)
                    print(f"{folder_type.capitalize()} folder is valid and contains playlists.")
                else:
                    self.handle_invalid_folder(folder_entry, checkmark_button, folder_type)
            else:
                self.handle_invalid_folder(folder_entry, checkmark_button, folder_type)
        else:
            self.handle_empty_folder(folder_entry, checkmark_button, folder_type)

    def select_folder(self, folder_type):
        """Open dialog to select a folder and validate it."""
        folder = filedialog.askdirectory(title=f"Select the {folder_type} Folder")
        if folder:
            if self.FOLDER_CONFIRMATION(folder):
                folder_entry = getattr(self, f"{folder_type.lower()}_entry")
                listbox = getattr(self, f"{folder_type.lower()}_listbox")
                checkmark_button = getattr(self, f"checkmark_button_{folder_type.lower()}")
                self.update_folder(folder, folder_entry, listbox, checkmark_button, folder_type.lower())
            else:
                self.handle_invalid_folder(folder_entry, checkmark_button, folder_type.lower())
        else:
            folder_entry = getattr(self, f"{folder_type.lower()}_entry")
            checkmark_button = getattr(self, f"checkmark_button_{folder_type.lower()}")
            self.handle_empty_folder(folder_entry, checkmark_button, folder_type.lower())

    def handle_invalid_folder(self, folder_entry, checkmark_button, folder_type):
        """Handle the case where the folder does not exist or contains no playlists."""
        folder_entry.delete(0, tk.END)
        messagebox.showwarning(f"No Playlists", f"The {folder_type} folder does not contain any playlists (.lpl files).")
        checkmark_button.config(bg="gray")
        print(f"No playlists found in the {folder_type} folder.")

    def handle_empty_folder(self, folder_entry, checkmark_button, folder_type):
        """Handle the case where the folder entry is empty."""
        checkmark_button.config(bg="gray")
        print(f"{folder_type.capitalize()} folder entry is empty.")

    def update_folder(self, folder, folder_entry, listbox, checkmark_button, folder_type):
        """Update the folder path and listbox UI elements."""
        setattr(self, f"{folder_type.upper()}_folder", folder)  # Update the instance variable (SOURCE or DESTINATION)
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)
        self.update_file_list(folder, listbox)
        checkmark_button.config(bg="lightgreen")

    def check_source(self):
        self.check_folder(self.source_entry, self.source_listbox, self.checkmark_button_source, "source")

    def check_destination(self):
        self.check_folder(self.destination_entry, self.destination_listbox, self.checkmark_button_destination, "destination")

    def on_folder_label_click(self, event, folder_type):
        """Generic method for folder label clicks to open folder selection dialogs."""
        self.select_folder(folder_type)

    def FOLDER_CONFIRMATION(self, strFolder):
        """Check if folder exists and contains .lpl files."""
        if strFolder:
            if os.path.exists(strFolder):
                lpl_files = glob.glob(os.path.join(strFolder, "*.lpl"))
                if lpl_files:
                    return True
                else:
                    messagebox.showwarning("No Playlists", f"The folder {strFolder} does not contain any playlists (.lpl files).")
                    return False
            else:
                messagebox.showerror("Folder Not Found", f"The folder {strFolder} does not exist.")
                return False
        return False

    def restart_app(self):
        """Clear paths, clear listboxes, and restart the file lists."""
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

            print("App has been restarted.")
        except Exception as e:
            print(f"Error in restart_app: {e}")

        self.backup_var.set(False)

    def backup_destination(self):
        """Backup the destination folder by copying .lpl files to a backup folder."""
        destination_folder = self.DESTINATION_folder
        if not destination_folder:
            messagebox.showerror("Error", "Destination folder not selected!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(destination_folder, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)

        for file_name in os.listdir(destination_folder):
            if file_name.endswith('.lpl'):
                source_file = os.path.join(destination_folder, file_name)
                backup_file = os.path.join(backup_folder, file_name)
                shutil.copy2(source_file, backup_file)

        print(f"Backup completed to {backup_folder}")

    def select_all(self):
        """Select all items in the destination listbox."""
        try:
            self.destination_listbox.select_set(0, tk.END)
        except Exception as e:
            print(f"Error in select_all: {e}")

    def clear_selection(self):
        """Deselect all items in the destination listbox."""
        try:
            self.destination_listbox.select_clear(0, tk.END)
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

    def show_about(self):
        """Show an 'About' message in a custom window with a fixed size."""
        show_about(self)

    def update_file_list(self, folder, listbox):
        """Update the file list in the listbox."""
        update_file_list(self, folder, listbox)
