import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_handler import process_folders
from gui.gui_utils import create_menu, create_widgets, show_about

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

    def create_widgets(self):
        """Create GUI components."""
        self.source_label = tk.Label(self.root, text="Source Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold"))
        self.source_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.DESTINATION_label = tk.Label(self.root, text="Destination Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold"))
        self.DESTINATION_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.source_listbox = tk.Listbox(self.root, height=10, width=30, font=("Helvetica", 10), bg="#FFFFFF", selectmode=tk.SINGLE, bd=2, relief="solid")
        self.source_listbox.grid(row=1, column=0, padx=20, pady=10)

        self.DESTINATION_listbox = tk.Listbox(self.root, height=10, width=30, font=("Helvetica", 10), bg="#FFFFFF", selectmode=tk.MULTIPLE, bd=2, relief="solid")
        self.DESTINATION_listbox.grid(row=1, column=1, padx=20, pady=10)

        self.select_all_button = tk.Button(self.root, text="Select All", command=self.select_all, bg="#4CAF50", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
        self.select_all_button.grid(row=2, column=1, padx=10, pady=5)

        self.clear_selection_button = tk.Button(self.root, text="Clear Selection", command=self.clear_selection, bg="#FF9800", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
        self.clear_selection_button.grid(row=3, column=1, padx=10, pady=5)

        self.execute_button = tk.Button(self.root, text="EXECUTE", command=self.execute, bg="#4CAF50", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
        self.execute_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.note_label = tk.Label(self.root, text=(
            "Only the selected playlists in the Destination list will be updated, "
            "if they exist in the Source list with the same name."
        ), bg="#F0F0F0", font=("Helvetica", 10), fg="gray")
        self.note_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.source_folder_label = tk.Label(self.root, text="No source folder selected", bg="#F0F0F0", font=("Helvetica", 10))
        self.source_folder_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.source_folder_label.bind("<Button-1>", self.on_source_folder_label_click)

        self.DESTINATION_folder_label = tk.Label(self.root, text="No destination folder selected", bg="#F0F0F0", font=("Helvetica", 10))
        self.DESTINATION_folder_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.DESTINATION_folder_label.bind("<Button-1>", self.on_DESTINATION_folder_label_click)

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_app, bg="#2196F3", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
        self.refresh_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

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
        listbox.delete(0, tk.END)  # Clear existing items
        try:
            files = [f for f in os.listdir(folder) if f.endswith(".lpl")]
            for file in files:
                listbox.insert(tk.END, file)
        except Exception as e:
            print(f"Error loading files: {e}")

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