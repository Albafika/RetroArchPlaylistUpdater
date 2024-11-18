from gui.app import PlaylistUpdaterApp
import tkinter as tk

def main():
    # Initialize the root Tkinter window
    root = tk.Tk()
    
    # Create an instance of the PlaylistUpdaterApp class
    app = PlaylistUpdaterApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()


#pyinstaller --onefile --windowed --icon=Undine.ico --add-data "Undine.ico;." --name RetroArchPlaylistUpdater main.py