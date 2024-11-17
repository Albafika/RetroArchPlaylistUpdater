import tkinter as tk
from tkinter import filedialog

def create_menu(app):
    """Create the menu bar with File and Help options."""
    menu_bar = tk.Menu(app.root, bg="#007ACC", fg="white", font=("Helvetica", 10))

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
    file_menu.add_command(label="Select Source Folder", command=app.select_source_folder)
    file_menu.add_command(label="Select Destination Folder", command=app.select_DESTINATION_folder)
    file_menu.add_command(label="Refresh", command=app.refresh_app)
    file_menu.add_command(label="Exit", command=app.exit_app)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0, bg="#0099FF", fg="white")
    help_menu.add_command(label="About", command=app.show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    app.root.config(menu=menu_bar)

def create_widgets(app):
    """Create GUI components."""
    # Source label
    app.source_label = tk.Label(app.root, text="Source Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold"))
    app.source_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Destination label
    app.DESTINATION_label = tk.Label(app.root, text="Destination Playlists", bg="#F0F0F0", font=("Helvetica", 12, "bold"))
    app.DESTINATION_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # Create listboxes for source and destination folder .lpl files
    app.source_listbox = tk.Listbox(app.root, height=10, width=30, font=("Helvetica", 10), bg="#FFFFFF", selectmode=tk.SINGLE, bd=2, relief="solid")
    app.source_listbox.grid(row=1, column=0, padx=20, pady=10)

    app.DESTINATION_listbox = tk.Listbox(app.root, height=10, width=30, font=("Helvetica", 10), bg="#FFFFFF", selectmode=tk.MULTIPLE, bd=2, relief="solid")
    app.DESTINATION_listbox.grid(row=1, column=1, padx=20, pady=10)

    # Folder path labels with clickable behavior
    app.source_folder_label = tk.Label(app.root, text="No source folder selected", bg="#F0F0F0", font=("Helvetica", 10))
    app.source_folder_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
    app.source_folder_label.bind("<Button-1>", app.on_source_folder_label_click)  # Bind click event to label

    app.DESTINATION_folder_label = tk.Label(app.root, text="No destination folder selected", bg="#F0F0F0", font=("Helvetica", 10))
    app.DESTINATION_folder_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
    app.DESTINATION_folder_label.bind("<Button-1>", app.on_DESTINATION_folder_label_click)  # Bind click event to label

    # Refresh button
    app.refresh_button = tk.Button(app.root, text="Refresh", command=app.refresh_app, bg="#2196F3", fg="white", font=("Helvetica", 12), bd=0, relief="solid")
    app.refresh_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def update_file_list(folder, listbox):
    """Update the file list in the listbox."""
    listbox.delete(0, tk.END)  # Clear existing items
    try:
        files = [f for f in os.listdir(folder) if f.endswith(".lpl")]
        for file in files:
            listbox.insert(tk.END, file)
    except Exception as e:
        print(f"Error loading files: {e}")

def show_about():
    """Show an 'About' message explaining what the app does and the required fields in the destination playlists."""
    about_text = (
        "Playlist Updater & Converter\n\n"
        "This tool helps you keep multiple instances of RetroArch's playlists synchronized (and most importantly, retain custom labels).\n"
        "It updates the playlists from a 'source' folder and copies the ROMs into a\n"
        "'destination' folder, making sure the paths and cores are consistent across all copies.\n\n"
        "Main features:\n\n"
        "1. Syncs ROM paths from the source playlist to the destination playlist.\n"
        "2. Replaces the core path and core name in the destination playlist with the default core set in the destination's settings.\n"
        "3. Updates each ROM's path based on the 'scan_content_dir' setting in the destination playlist.\n\n"
        "Required fields in the destination playlist for this app to work correctly:\n\n"
        "1. **default_core_path**: Path to the default core that will be used for the ROMs in the playlist.\n"
        "2. **default_core_name**: Name of the default core to use for the ROMs in the playlist.\n"
        "3. **scan_content_dir**: Directory where the ROMs are stored, which will be used to update ROM paths.\n\n"
        "This app is perfect for maintaining consistency across local setups, USB drives, and even consoles.\n\n"
        "For any questions, bug reports, or feature requests, feel free to contact me:\n"
        "Email: goodlucktrying00@gmail.com\n"
        "Discord: GoodLuckTrying\n"
        "GitHub: https://github.com/Albafika/RetroArchPlaylistUpdater\n"
        "I'll do my best to assist you!"
    )
    messagebox.showinfo("About", about_text)
