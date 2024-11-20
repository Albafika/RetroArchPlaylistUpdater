import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_menu(self):
    """Create the menu bar with File and Help options."""
    menu_bar = tk.Menu(self.root, bg="#007ACC", fg="white", font=("Helvetica", 10))

    file_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
    file_menu.add_command(label="Select Source Folder", command=lambda: self.select_folder("SOURCE"))
    file_menu.add_command(label="Select Destination Folder", command=lambda: self.select_folder("DESTINATION"))
    file_menu.add_command(label="Restart", command=self.restart_app)
    file_menu.add_command(label="Exit", command=self.exit_app)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
    help_menu.add_command(label="About", command=self.show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    self.root.config(menu=menu_bar)

def create_widgets(self):
    # Configure the root grid layout
    self.root.grid_columnconfigure(0, weight=0)  # Label column
    self.root.grid_columnconfigure(1, weight=1)  # Entry/Listbox column (expandable)
    self.root.grid_columnconfigure(2, weight=0)  # Button column

    # Frame for source and destination selection
    folder_frame = tk.Frame(self.root, bg="#F0F0F0", padx=10, pady=5)
    folder_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

    # Source Folder
    tk.Label(folder_frame, text="Source Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    self.source_entry = tk.Entry(folder_frame, width=50)
    self.source_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    # Checkmark button next to source_entry
    self.checkmark_button_source = tk.Button(folder_frame, text="✓", command=lambda: self.check_folder(self.source_entry, self.source_listbox, self.checkmark_button_source, "SOURCE"), width=2, height=1, font=("Helvetica", 10))
    self.checkmark_button_source.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="e")
    # Browse button for source folder
    tk.Button(folder_frame, text="Browse", command=lambda: self.select_folder("SOURCE")).grid(row=0, column=2, padx=5, pady=5)

    # Destination Folder
    tk.Label(folder_frame, text="Destination Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    self.destination_entry = tk.Entry(folder_frame, width=40)
    self.destination_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    # Checkmark button next to destination_entry
    self.checkmark_button_destination = tk.Button(folder_frame, text="✓", command=lambda: self.check_folder(self.destination_entry, self.destination_listbox, self.checkmark_button_destination, "DESTINATION"), width=2, height=1, font=("Helvetica", 10))
    self.checkmark_button_destination.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="e")
    # Browse button for destination folder
    tk.Button(folder_frame, text="Browse", command=lambda: self.select_folder("DESTINATION")).grid(row=1, column=2, padx=5, pady=5)

    # Frame for playlist listboxes
    playlist_frame = tk.Frame(self.root, bg="#F0F0F0", padx=10, pady=10)
    playlist_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

    # Source Playlists
    tk.Label(playlist_frame, text="Source Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
    self.source_listbox = tk.Listbox(playlist_frame, height=10, width=30, font=("Helvetica", 10), bd=2, relief="solid")
    self.source_listbox.grid(row=1, column=0, padx=10, pady=5)

    # Destination Playlists
    tk.Label(playlist_frame, text="Destination Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
    self.destination_listbox = tk.Listbox(playlist_frame, height=10, width=30, font=("Helvetica", 10), bd=2, relief="solid", selectmode=tk.MULTIPLE)
    self.destination_listbox.grid(row=1, column=1, padx=10, pady=5)

    # Buttons for Options
    tk.Button(playlist_frame, text="Restart", command=self.restart_app, bg="#2196F3", fg="white", font=("Helvetica", 12), bd=0, relief="solid").grid(row=2, column=0, padx=10, pady=5)
    tk.Checkbutton(playlist_frame, text="Backup Destination Playlists", variable=self.backup_var, bg="#F0F0F0", font=("Helvetica", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Button(playlist_frame, text="Select All", command=self.select_all, bg="#4CAF50", fg="white", font=("Helvetica", 12), bd=0, relief="solid").grid(row=2, column=1, padx=10, pady=5)
    tk.Button(playlist_frame, text="Clear Selection", command=self.clear_selection, bg="#FF9800", fg="white", font=("Helvetica", 12), bd=0, relief="solid").grid(row=3, column=1, padx=10, pady=5)

    # Execute Button
    self.execute_button = tk.Button(self.root, text="EXECUTE", command=self.execute, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), bd=0, relief="solid")
    self.execute_button.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky="n")

    # Note Label
    tk.Label(self.root, text=( 
        "Only the selected playlists in the Destination list will be updated, "
        "if they exist in the Source list with the same name."
    ), bg="#F0F0F0", font=("Helvetica", 10), fg="gray", wraplength=500, justify="center").grid(row=3, column=0, columnspan=3, padx=10, pady=10)

def update_file_list(self, folder, listbox):
    """Update the file list in the listbox."""
    listbox.delete(0, tk.END)  # Clear existing items
    try:
        # Check if the directory exists
        if os.path.exists(folder):
            # Get all files with the .lpl extension in the selected folder
            files = [f for f in os.listdir(folder) if f.endswith(".lpl")]
            if files:
                for file in files:
                    listbox.insert(tk.END, file)  # Insert file names into the listbox
            else:
                listbox.insert(tk.END, "No .lpl files found.")  # Message when no files found
        else:
            print(f"Error: Folder '{folder}' does not exist.")
    except Exception as e:
        print(f"Error loading files: {e}")

def show_about(app):
    """Show an 'About' message in a custom window with a fixed size."""
    about_window = tk.Toplevel(app.root)
    about_window.title("About")
    about_window.geometry("700x500")
    about_window.resizable(False, False)  # Make the window non-resizable

    # Add a Text widget with a scrollbar for displaying the about text
    text_frame = tk.Frame(about_window, bg="#F0F0F0")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    about_text = (
        "RetroArch Playlist Updater & Synchronizer 1.2 by GoodLuckTrying\n\n"
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
        "GitHub: https://github.com/GoodLuckTrying/RetroArchPlaylistUpdater\n"
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