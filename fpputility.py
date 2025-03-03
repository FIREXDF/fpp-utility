import zipfile
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Scrollbar, Listbox

def get_all_files_and_dirs(directory):
    """Recursively retrieves all files and directories from the given directory."""
    file_list = []
    dir_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, directory)
            file_list.append((full_path, relative_path))

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            rel_dir_path = os.path.relpath(dir_path, directory)
            dir_list.append(rel_dir_path)

    return file_list, dir_list

def create_fpp(output_filename, mods_directory="mods", plugins_directory="plugins", progress_label=None):
    """Creates a FightPlannerPackage (.fpp) including all files and directories under mods and plugins."""
    if not os.path.exists(mods_directory) or not os.path.exists(plugins_directory):
        messagebox.showerror("Error", f"One of the folders '{mods_directory}' or '{plugins_directory}' does not exist.")
        return

    mods_files, mods_dirs = get_all_files_and_dirs(mods_directory)
    plugins_files, plugins_dirs = get_all_files_and_dirs(plugins_directory)

    if progress_label:
        progress_label.config(text="Creating FPP...")

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as fpp:
        # Creating the manifest with plugins and mods directories
        manifest = {
            "version": 1,
            "mods_files": [rel_path for _, rel_path in mods_files],
            "plugins_files": [rel_path for _, rel_path in plugins_files],
            "mods_directories": mods_dirs,
            "plugins_directories": plugins_dirs
        }
        fpp.writestr("manifest.json", json.dumps(manifest, indent=2))

        # Adding mods files to the 'mods' folder in the archive
        for full_path, rel_path in mods_files:
            fpp.write(full_path, f"mods/{rel_path}")

        # Adding plugins files to the 'plugins' folder in the archive
        for full_path, rel_path in plugins_files:
            fpp.write(full_path, f"plugins/{rel_path}")

        # Adding empty directories for mods and plugins
        for dir_path in mods_dirs:
            fpp.writestr(f"mods/{dir_path}/", "")  # Create empty directory in mods

        for dir_path in plugins_dirs:
            fpp.writestr(f"plugins/{dir_path}/", "")  # Create empty directory in plugins

    if progress_label:
        progress_label.config(text="FightPlannerPackage created successfully!")
    messagebox.showinfo("Success", f"FightPlannerPackage created: {output_filename}")

def extract_fpp(filename, output_directory, progress_label=None):
    """Extracts a FightPlannerPackage (.fpp) while preserving files and empty directories."""
    with zipfile.ZipFile(filename, 'r') as fpp:
        # Reading the manifest from the .fpp file
        manifest = json.loads(fpp.read("manifest.json"))

        if progress_label:
            progress_label.config(text="Extracting...")

        # Extracting files
        fpp.extractall(output_directory)  # Extract files to the chosen folder

        # Creating empty directories if needed
        for dir_path in manifest["mods_directories"]:
            dir_full_path = os.path.join(output_directory, "mods", dir_path)
            os.makedirs(dir_full_path, exist_ok=True)  # Create empty directory if it doesn't exist

        for dir_path in manifest["plugins_directories"]:
            dir_full_path = os.path.join(output_directory, "plugins", dir_path)
            os.makedirs(dir_full_path, exist_ok=True)  # Create empty directory if it doesn't exist

    if progress_label:
        progress_label.config(text="Extraction completed successfully!")
    messagebox.showinfo("Success", f"Files extracted to: {output_directory}")

def list_fpp_files(filename):
    """Lists the files and directories inside a .fpp file."""
    with zipfile.ZipFile(filename, 'r') as fpp:
        # Reading the manifest from the .fpp file
        manifest = json.loads(fpp.read("manifest.json"))

    return manifest["mods_files"], manifest["plugins_files"], manifest["mods_directories"], manifest["plugins_directories"]

class FPPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FightPlannerPackage Manager")

        # Main frame
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        # Status label
        self.progress_label = tk.Label(self.frame, text="", fg="green", font=("Arial", 12))
        self.progress_label.pack(pady=10)

        # Create FPP button
        self.create_button = tk.Button(self.frame, text="Create FightPlannerPackage (.fpp)", command=self.create_fpp)
        self.create_button.pack(pady=10)

        # Extract FPP button
        self.extract_button = tk.Button(self.frame, text="Extract FightPlannerPackage (.fpp)", command=self.extract_fpp)
        self.extract_button.pack(pady=10)

        # List FPP files button
        self.list_button = tk.Button(self.frame, text="List files in a FightPlannerPackage", command=self.list_fpp)
        self.list_button.pack(pady=10)

    def create_fpp(self):
        mods_folder = filedialog.askdirectory(title="Select the mods folder")
        plugins_folder = filedialog.askdirectory(title="Select the plugins folder")
        if mods_folder and plugins_folder:
            filename = filedialog.asksaveasfilename(defaultextension=".fpp", filetypes=[("FPP Files", "*.fpp")], title="Save FightPlannerPackage")
            if filename:
                self.progress_label.config(text="Creating FPP...")
                create_fpp(filename, mods_folder, plugins_folder, self.progress_label)

    def extract_fpp(self):
        file = filedialog.askopenfilename(filetypes=[("FPP Files", "*.fpp")], title="Select a FightPlannerPackage file")
        if file:
            folder = filedialog.askdirectory(title="Choose the extraction folder")
            if folder:
                self.progress_label.config(text="Extracting...")
                extract_fpp(file, folder, self.progress_label)

    def list_fpp(self):
        file = filedialog.askopenfilename(filetypes=[("FPP Files", "*.fpp")], title="Select a FightPlannerPackage file")
        if file:
            mods_files, plugins_files, mods_dirs, plugins_dirs = list_fpp_files(file)
            # Create a new window to show the file and directory list
            list_window = Toplevel(self.root)
            list_window.title("Files and Directories in the FPP")

            # Scrollbar for the list
            scrollbar = Scrollbar(list_window)
            scrollbar.pack(side="right", fill="y")

            # Listbox to display the files and directories
            listbox = Listbox(list_window, selectmode=tk.SINGLE, width=80, height=20)
            listbox.pack(padx=10, pady=10)
            scrollbar.config(command=listbox.yview)
            listbox.config(yscrollcommand=scrollbar.set)

            # Insert mods files into the listbox
            listbox.insert(tk.END, "Mods Files:")
            for file in mods_files:
                listbox.insert(tk.END, file)

            # Insert plugins files into the listbox
            listbox.insert(tk.END, "\nPlugins Files:")
            for file in plugins_files:
                listbox.insert(tk.END, file)

            # Insert mods directories into the listbox
            listbox.insert(tk.END, "\nMods Directories:")
            for directory in mods_dirs:
                listbox.insert(tk.END, directory)

            # Insert plugins directories into the listbox
            listbox.insert(tk.END, "\nPlugins Directories:")
            for directory in plugins_dirs:
                listbox.insert(tk.END, directory)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FPPApp(root)
    root.mainloop()
