import subprocess
import tkinter as tk

def run_script():
    script_path = r"C:\Users\scrim\OneDrive - Aston University\Documents\Work\Research Associate\pupil\pupil_src\synchronization_script1.ps1"
    subprocess.Popen(["powershell", "-File", script_path])
    record_button.config(state=tk.DISABLED)
    window.after(60000, enable_button)

def enable_button():
    record_button.config(state=tk.NORMAL)

# Create the main window
window = tk.Tk()

# Set window title
window.title("Experiment Recorder")

# Set window dimensions
window.geometry("300x200")

# Create the 'Record' button
record_button = tk.Button(window, text="Record", command=run_script)
record_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Run the GUI event loop
window.mainloop()
