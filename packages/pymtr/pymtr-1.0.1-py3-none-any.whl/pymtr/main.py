import psutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from operator import itemgetter
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt

class ProcessMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("Process Monitor")

        self.sort_column = 'cpu_percent'
        self.sort_direction = 'desc'
        self.num_processes_to_display = -1  # Display all processes by default
        self.update_interval = 5  # Default update interval in seconds

        # Current system information
        self.system_info_label = tk.Label(master, text="", justify="left")
        self.system_info_label.grid(row=0, column=0, columnspan=2, sticky="w")

        # Process list with header
        self.tree = ttk.Treeview(master, columns=('PID', 'Process name', 'Username', 'CPU %', 'Memory %'), show='headings')
        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=1, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree.column('PID', width=100)
        self.tree.column('Process name', width=200)
        self.tree.column('Username', width=150)
        self.tree.column('CPU %', width=100)
        self.tree.column('Memory %', width=100)

        self.tree.heading('PID', text='PID', command=lambda: self.sort_by_column('pid'))
        self.tree.heading('Process name', text='Process name', command=lambda: self.sort_by_column('name'))
        self.tree.heading('Username', text='Username', command=lambda: self.sort_by_column('username'))
        self.tree.heading('CPU %', text='CPU %', command=lambda: self.sort_by_column('cpu_percent'))
        self.tree.heading('Memory %', text='Memory %', command=lambda: self.sort_by_column('memory_percent'))

        # Number of processes entry
        self.num_processes_label = tk.Label(master, text="Number of processes to display:")
        self.num_processes_label.grid(row=2, column=0, sticky="w")
        self.num_processes_entry = tk.Entry(master, width=10)
        self.num_processes_entry.grid(row=2, column=1, sticky="ew")
        self.num_processes_entry.insert(0, 'All')

        # Update interval entry
        self.update_interval_label = tk.Label(master, text="Update interval (seconds):")
        self.update_interval_label.grid(row=3, column=0, sticky="w")
        self.update_interval_entry = tk.Entry(master, width=10)
        self.update_interval_entry.grid(row=3, column=1, sticky="ew")
        self.update_interval_entry.insert(0, str(self.update_interval))

        # Instructions label
        self.instructions_label = tk.Label(master, text="Press 'h' to show help page, or 'q' to quit.", justify="left")
        self.instructions_label.grid(row=4, column=0, columnspan=2, sticky="w")
        self.instructions_label.bind("<Configure>", self.wrap_text)

        # Save button
        self.save_button = tk.Button(master, text="Save", command=self.save_to_file)
        self.save_button.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.tree.bind('<ButtonRelease-1>', self.on_click)
        self.master.bind('k', self.kill_selected_process)
        self.master.bind('h', self.show_help)
        self.master.bind('<Shift-C>', self.create_cpu_pie_chart)

        self.update_system_info()
        self.update_process_list()
        self.start_periodic_updates()

    def wrap_text(self, event):
        self.instructions_label.configure(wraplength=self.master.winfo_width())

    def update_system_info(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime = str(timedelta(seconds=uptime_seconds))
        uptime = datetime.strptime(uptime.split(".")[0], "%H:%M:%S").strftime("%H:%M:%S")
        num_users = len(psutil.users())
        num_processes = len(psutil.pids())
        mem = psutil.virtual_memory()
        ram_free = mem.available / (1024 ** 3)  # Convert to GB
        ram_used = mem.used / (1024 ** 3)  # Convert to GB
        disk = psutil.disk_usage('/')
        disk_free = disk.free / (1024 ** 3)  # Convert to GB
        disk_used = disk.used / (1024 ** 3)  # Convert to GB

        system_info_text = f"Current Time: {current_time}\nUptime: {uptime}\nNumber of Users: {num_users}\nNumber of Processes: {num_processes}\nFree RAM: {ram_free:.2f} GB / Used RAM: {ram_used:.2f} GB\nFree Disk: {disk_free:.2f} GB / Used Disk: {disk_used:.2f} GB"
        self.system_info_label.config(text=system_info_text)
        self.master.after(1000, self.update_system_info)

    def update_process_list(self):
        self.tree.delete(*self.tree.get_children())  # Delete old data
        processes = self.get_process_info()[:self.num_processes_to_display]
        for proc in processes:
            pid = "{:<10}".format(proc['pid'])
            name = "{:<25}".format(proc['name'])
            username = "{:<15}".format(proc['username'])
            cpu_percent = "{:<15.2f}".format(proc['cpu_percent'])
            memory_percent = "{:<10.2f}".format(proc['memory_percent'])
            self.tree.insert('', 'end', values=(pid, name, username, cpu_percent, memory_percent))

    def get_process_info(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            process_info = proc.info
            try:
                username = proc.username()
            except psutil.AccessDenied:
                username = 'N/A'
            process_info['username'] = username
            processes.append(process_info)
        if self.sort_column == 'name':
            processes.sort(key=itemgetter('name'), reverse=self.sort_direction == 'desc')
        elif self.sort_column == 'pid':
            processes.sort(key=itemgetter('pid'), reverse=self.sort_direction == 'desc')
        elif self.sort_column == 'username':
            processes.sort(key=itemgetter('username'), reverse=self.sort_direction == 'desc')
        else:
            processes.sort(key=itemgetter(self.sort_column), reverse=self.sort_direction == 'desc')
        return processes

    def sort_by_column(self, column):
        if self.sort_column == column:
            self.sort_direction = 'asc' if self.sort_direction == 'desc' else 'desc'
        else:
            self.sort_column = column
            self.sort_direction = 'desc'
        self.update_process_list()

    def quit_app(self):
        self.master.quit()

    def start_periodic_updates(self):
        self.master.after(1000 * self.update_interval, self.update_process_list)
        self.master.after(1000 * self.update_interval, self.start_periodic_updates)

    def update_num_processes(self, event=None):
        try:
            num_processes = self.num_processes_entry.get()
            if num_processes.lower() == 'all':
                self.num_processes_to_display = -1  # Display all processes
            else:
                num_processes = int(num_processes)
                if num_processes > 0:
                    self.num_processes_to_display = num_processes
            self.update_process_list()
        except ValueError:
            pass

    def update_update_interval(self, event=None):
        try:
            update_interval = int(self.update_interval_entry.get())
            if update_interval > 0:
                self.update_interval = update_interval
                self.start_periodic_updates()
        except ValueError:
            pass

    def on_click(self, event):
        item = self.tree.selection()[0]
        self.selected_pid = self.tree.item(item, 'values')[0]

    def kill_selected_process(self, event):
        try:
            selected_pid = int(self.selected_pid)
            psutil.Process(selected_pid).terminate()
            self.update_process_list()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def create_cpu_pie_chart(self, event):
        processes = self.get_process_info()[:7]  # Get top 7 CPU usage processes
        labels = [proc['name'] for proc in processes]
        sizes = [proc['cpu_percent'] for proc in processes]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Top 7 CPU Usage Processes')
        plt.show()

    def show_help(self, event):
        help_window = tk.Toplevel(self.master)
        help_window.title("Help")
        help_text = """
        Hotkeys:
        'c' - Sort by CPU %
        'm' - Sort by Memory %
        'p' - Sort by PID
        'n' - Sort by Process name
        'u' - Sort by Username
        'k' - Kill selected process
        'h' - Show this help message
        'Shift+C' - Create CPU Pie Chart
        
        Sort by clicking on column headers.
        """
        tk.Label(help_window, text=help_text, justify="left").pack()

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                # Write system information
                file.write("System Information:\n")
                file.write(self.system_info_label.cget("text") + "\n\n")
                # Write process information
                file.write("Process Information:\n")
                # Write column names
                column_names = [self.tree.heading(col)["text"] for col in self.tree["columns"]]
                file.write("\t".join(column_names) + "\n")
                for child in self.tree.get_children():
                    values = self.tree.item(child, "values")
                    file.write("\t".join(values) + "\n")
            messagebox.showinfo("Save", "File saved successfully.")

def main():
    root = tk.Tk()
    app = ProcessMonitorApp(root)
    root.bind('c', lambda event: app.sort_by_column('cpu_percent'))
    root.bind('m', lambda event: app.sort_by_column('memory_percent'))
    root.bind('p', lambda event: app.sort_by_column('pid'))
    root.bind('n', lambda event: app.sort_by_column('name'))
    root.bind('u', lambda event: app.sort_by_column('username'))
    root.bind('q', lambda event: app.quit_app())
    app.num_processes_entry.bind('<Return>', app.update_num_processes)  # Bind Enter key to update number of processes
    app.update_interval_entry.bind('<Return>', app.update_update_interval)  # Bind Enter key to update update interval
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()

