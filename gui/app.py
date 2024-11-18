import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.json_handler import load_json, save_json, modify_json_file
from utils.file_handler import process_folders

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
        self.create_menu()

        # Create the UI components
        self.create_widgets()

    def create_menu(self):
        """Create the menu bar with File and Help options."""
        menu_bar = tk.Menu(self.root, bg="#007ACC", fg="white", font=("Helvetica", 10))

        file_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
        file_menu.add_command(label="Select Source Folder", command=self.select_source_folder)
        file_menu.add_command(label="Select Destination Folder", command=self.select_DESTINATION_folder)
        file_menu.add_command(label="Refresh", command=self.refresh_app)
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

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
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("700x500")
        about_window.resizable(False, False)  # Make the window non-resizable

        # Add a Text widget with a scrollbar for displaying the about text
        text_frame = tk.Frame(about_window, bg="#F0F0F0")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        about_text = (
            "RetroArch Playlist Updater & Synchronizer by GoodLuckTrying\n\n"
            "- This tool helps you keep multiple instances of RetroArch's playlists (.lpl) in parity (and most importantly, retain custom labels).\n"
            "- It does not update your ROMs or ROM folders.\n"
            "- It copies all listed ROMs from the source playlist to the destination playlist (Update will only happen between playlists sharing name between folders).\n\n"
            "Main features:\n"
            "1. Copy ROMs from source playlists to destination playlists while retaining custom labels.\n"
            "2. Update core paths and names in destination playlists.\n"
            "3. Adjust destination playlists' ROM paths using scan_content_dir\n\n"
            "Required fields in the **destination playlist** for this app to work correctly:\n"
            "1. **default_core_path**: Path to the default core that will be used for the ROMs.\n"
            "2. **default_core_name**: Name of the default core to use for the ROMs.\n"
            "3. **scan_content_dir**: Directory where the ROMs are stored, which will be used to update ROM paths.\n\n"
            "This app is perfect for maintaining ROM playlist parity across local setups, USB drives, and even consoles.\n\n"
            "For any questions, bug reports, or feature requests, feel free to contact me:\n"
            "Email: goodlucktrying00@gmail.com\n"
            "Discord: GoodLuckTrying\n"
            "GitHub: https://github.com/Albafika/RetroArchPlaylistUpdater\n"
            "I'll do my best to assist you!"
        )

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Helvetica", 10), bg="#F0F0F0", fg="black", bd=0)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        # Add a Close button
        close_button = tk.Button(about_window, text="Close", command=about_window.destroy, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        close_button.pack(pady=10)

