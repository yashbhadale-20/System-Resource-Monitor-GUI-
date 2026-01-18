import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import os
import signal

root = tk.Tk()
root.title("System Resource Monitor")
root.geometry("800x500")
root.config(bg="#1e1e1e")

# ------------------ System Stats ------------------
def update_stats():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    ram_label.config(text=f"RAM Usage: {memory.percent}%")
    disk_label.config(text=f"Disk Usage: {disk.percent}%")

    root.after(1000, update_stats)

# ------------------ Process List ------------------
def load_processes():
    process_table.delete(*process_table.get_children())
    for proc in psutil.process_iter(['pid', 'name']):
        process_table.insert("", "end", values=(proc.info['pid'], proc.info['name']))

# ------------------ Kill Process ------------------
def kill_process():
    selected = process_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a process first!")
        return

    pid = int(process_table.item(selected)['values'][0])
    try:
        os.kill(pid, signal.SIGTERM)
        messagebox.showinfo("Success", f"Process {pid} killed")
        load_processes()
    except PermissionError:
        messagebox.showerror("Error", "Permission denied")

# ------------------ UI ------------------
title = tk.Label(root, text="System Resource Monitor", fg="white",
                 bg="#1e1e1e", font=("Arial", 18, "bold"))
title.pack(pady=10)

cpu_label = tk.Label(root, fg="white", bg="#1e1e1e", font=("Arial", 12))
ram_label = tk.Label(root, fg="white", bg="#1e1e1e", font=("Arial", 12))
disk_label = tk.Label(root, fg="white", bg="#1e1e1e", font=("Arial", 12))

cpu_label.pack()
ram_label.pack()
disk_label.pack()

# Process Table
columns = ("PID", "Process Name")
process_table = ttk.Treeview(root, columns=columns, show="headings")
process_table.heading("PID", text="PID")
process_table.heading("Process Name", text="Process Name")
process_table.pack(fill="both", expand=True, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack()

refresh_btn = tk.Button(btn_frame, text="Refresh Processes",
                        command=load_processes)
refresh_btn.pack(side="left", padx=10)

kill_btn = tk.Button(btn_frame, text="Kill Process",
                     command=kill_process, bg="red", fg="white")
kill_btn.pack(side="left")

# Start
load_processes()
update_stats()
root.mainloop()
