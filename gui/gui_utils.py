import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_menu(app):
    """Create the menu bar with File and Help options."""
    menu_bar = tk.Menu(app.root, bg="#007ACC", fg="white", font=("Helvetica", 10))

    file_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
    file_menu.add_command(label="Select Source Folder", command=app.select_source_folder)
    file_menu.add_command(label="Select Destination Folder", command=app.select_DESTINATION_folder)
    file_menu.add_command(label="Refresh", command=app.refresh_app)
    file_menu.add_command(label="Exit", command=app.exit_app)
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
    help_menu.add_command(label="About", command=app.show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    app.root.config(menu=menu_bar)

def create_widgets(app):
    """Create GUI components."""
    app.source_label = tk.Label(app.root, text="Source Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold"))
    app.source_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    app.DESTINATION_label = tk.Label(app.root, text="Destination Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold"))
    app.DESTINATION_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    app.source_listbox = tk.Listbox(app.root, height=10, width=30, font=("Helvetica", 10), bg="#FFFFFF", selectmode=tk.SINGLE, bd=2, relief="solid")
    app.source_listbox.grid(row=1, column=0, padx=20, pady=10)

    app.DESTINATION_listbox = tk.Listbox(app.root, height=10, width=30, font=("Helvetica", 10), bg="#FFFFFF", selectmode=tk.MULTIPLE, bd=2, relief="solid")
    app.DESTINATION_listbox.grid(row=1, column=1, padx=20, pady=10)

    app.select_all_button = tk.Button(app.root, text="Select All", command=app.select_all, bg="#4CAF50", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
    app.select_all_button.grid(row=2, column=1, padx=10, pady=5)

    app.clear_selection_button = tk.Button(app.root, text="Clear Selection", command=app.clear_selection, bg="#FF9800", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
    app.clear_selection_button.grid(row=3, column=1, padx=10, pady=5)

    app.execute_button = tk.Button(app.root, text="EXECUTE", command=app.execute, bg="#4CAF50", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
    app.execute_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    app.note_label = tk.Label(app.root, text=(
        "Only the selected playlists in the Destination list will be updated, "
        "if they exist in the Source list with the same name."
    ), bg="#F0F0F0", font=("Helvetica", 10), fg="gray")
    app.note_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    app.source_folder_label = tk.Label(app.root, text="No source folder selected", bg="#F0F0F0", font=("Helvetica", 10))
    app.source_folder_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
    app.source_folder_label.bind("<Button-1>", app.on_source_folder_label_click)

    app.DESTINATION_folder_label = tk.Label(app.root, text="No destination folder selected", bg="#F0F0F0", font=("Helvetica", 10))
    app.DESTINATION_folder_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
    app.DESTINATION_folder_label.bind("<Button-1>", app.on_DESTINATION_folder_label_click)

    app.refresh_button = tk.Button(app.root, text="Refresh", command=app.refresh_app, bg="#2196F3", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
    app.refresh_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def update_file_list(app, folder, listbox):
    """Update the file list in the listbox."""
    listbox.delete(0, tk.END)  # Clear existing items
    try:
        files = [f for f in os.listdir(folder) if f.endswith(".lpl")]
        for file in files:
            listbox.insert(tk.END, file)
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