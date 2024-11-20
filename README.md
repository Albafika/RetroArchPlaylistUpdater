# RetroArch Playlist Updater

## Overview

The **Playlist Updater** is a Python application designed to **update RetroArch playlist files** (`.lpl`) by synchronizing ROMs between source and destination playlists. It ensures playlist rom parity across multiple directories, whether local setups, USB drives, gaming consoles, etc.

### Main Appeal

The **main appeal** is the ability to **copy ROMs** from **source playlists** to **destination playlists** while **retaining custom labels**, ideal for syncing playlists across systems without losing personal settings.

This tool is only for those that want to keep their playlists/roms the same in several locations (Say, you have the exact same SNES Roms/Romhacks in your PC emulator and your USB/Console, but now you want to add more while retaining your labels and updating all the different setups' playlists is a chore). Instead of manually refreshing/rebuilding the playlists/.lpl everywhere (your portable USB setup, your console setup, etc.), you only fix one playlist group (Say, PC's setup) and then this app updates the changes in the other chosen setups for you.

### What It Does

The tool modifies **destination playlists** (`.lpl`) by:

- **Copying all ROMs** from the source playlist to the destination playlist (Update will only happen between playlists sharing name between folders).
- **Retaining custom labels** when copying ROM entries.
- **Updating core paths** and **core names** in the destination with defaults from the destination’s config.
- **Adjusting ROM paths** based on the `scan_content_dir` in the destination playlist.

### Important Requirements

For proper operation, the **destination playlist** must contain:

- **default_core_path**: Path to the core for the ROMs.
- **default_core_name**: Name of the default core.
- **scan_content_dir**: Directory where the ROMs are stored.

#### Example of Required Fields in Destination Playlist:

```json
{
  "default_core_path": "Z:\\RetroArch\\cores\\mgba_libretro.dll",
  "default_core_name": "Nintendo - Game Boy Advance (mGBA)",
  "scan_content_dir": "D:\\RetroArch\\Emulator\\Game Boy Advance\\Roms"
}
```
In this example:

- The **default_core_path** specifies the full path to the core `mgba_libretro.dll`, which will be used for Game Boy Advance ROMs in the playlist.
- The **default_core_name** provides the name of the core, which helps RetroArch identify the emulator to use.
- The **scan_content_dir** points to the folder where the Game Boy Advance ROMs are located (`D:\\RetroArch\\Emulator\\Game Boy Advance\\Roms`). This is the directory where the ROM paths in the playlist will be updated to (It'll also work if the path contains `\`, `/` or `//` in the paths).

If any fields are missing or incorrect, the tool won’t update the playlist correctly.

## Features

- **Copy ROMs** from source playlists to destination playlists **while retaining custom labels**.
- **Update core paths and names** in destination playlists.
- **Adjust ROM paths** using `scan_content_dir`.
- Playlists must **have the same name** for the update to work.
- User-friendly **GUI** built with `Tkinter`.

## Dependencies

- Python 3.x
- `tkinter`
- `json`
- `os`

---

## Usage

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Albafika/RetroArchPlaylistUpdater.git
    cd RetroArchPlaylistUpdater
    ```

2. **Run the Application**:

    ```bash
    python main.py
    ```

    The GUI will launch, allowing you to:

3. **Select Source and Destination Folders**:
    - Click **File** > **Select Source Folder** to choose the source playlist folder.
    - Click **Select Destination Folder** to choose the destination playlist folder.

4. **Select Playlists**:
    - Select playlists you wish to update in the "Destination Playlists" list.
    - Use **Select All** to select all playlists in the destination folder.

5. **Execute the Update**:
    - Click **EXECUTE** to update the selected playlists in the Destination list with the ROMs listed in the Source playlists.

* **Restart the App**:
    - Click **Restart** to pretty much initialize the app with paths and checks cleared.

* **Backup Destination Playlists**:
    - Check  **Backup Destination Playlists** if you wish for the destination's playlists to be backed up in a folder in the same path (Folder will be named "backup_" + "current date").

 * **About the Application**:
    - View app details by selecting **Help > About**.

### Notes:
- Playlists **must have the same name** in both folders to be updated.
- Only selected playlists in the **Destination Folder** will be updated.

---

## Building an Executable

1. **Install PyInstaller**:

    ```bash
    pip install pyinstaller
    ```

2. **Build the Executable**:

    ```bash
    pyinstaller --onefile --windowed --icon=Undine.ico --add-data "Undine.ico;." --name RetroArchPlaylistUpdater main.py
    ```

3. **Locate the Executable**:
    - Find the `.exe` in the `dist` folder for distribution.

## License

This project is licensed under the GPL-3.0 license.

## About the Author

For questions or feature requests, contact:

- Email: goodlucktrying00@gmail.com
- Discord: GoodLuckTrying
- GitHub: [GoodLuckTrying/RetroArchPlaylistUpdater](https://github.com/GoodLuckTrying/RetroArchPlaylistUpdater)
