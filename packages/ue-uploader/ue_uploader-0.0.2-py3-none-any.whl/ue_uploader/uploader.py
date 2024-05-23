import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from library_up import Programmer


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CH55x Programmer")
        self.geometry("300x400")
        self.programmer = None
        self.device_detected = False

        # Style configuration
        self.style = ttk.Style(self)
        self.style.configure("TButton", padding=10, font=("Helvetica", 12))
        self.style.map("TButton",
                       foreground=[("active", "blue"), ("disabled", "gray")],
                       background=[("active", "lightgray"), ("disabled", "gray")])

        # Buttons
        self.create_buttons()
        self.create_version_label()

    def create_buttons(self):
        ttk.Button(self, text="Connect", command=self.connect_and_detect).pack(pady=5)
        self.erase_button = ttk.Button(self, text="Erase Chip", command=self.erase_chip, state="disabled")
        self.erase_button.pack(pady=5)
        self.flash_button = ttk.Button(self, text="Flash Firmware", command=self.flash_firmware, state="disabled")
        self.flash_button.pack(pady=5)
        self.verify_button = ttk.Button(self, text="Verify Firmware", command=self.verify_firmware, state="disabled")
        self.verify_button.pack(pady=5)
        ttk.Button(self, text="Exit Program", command=self.exit_program).pack(pady=5)
        ttk.Button(self, text="Run Programmer Exit", command=self.run_programmer_exit).pack(pady=5)

    def create_version_label(self):
        ttk.Label(self, text="UNITloader Version: 0.1", font=("Helvetica", 7)).pack(pady=5)

    def connect_and_detect(self):
        try:
            self.programmer = Programmer()
            self.programmer.detect()
            self.device_detected = True
            self.update_button_state()
            messagebox.showinfo("Success", "Device connected and chip detected: " + self.programmer.chipname)
        except Exception as e:
            self.device_detected = False
            messagebox.showerror("Error", str(e))

    def update_button_state(self):
        self.erase_button.config(state="normal")
        self.flash_button.config(state="normal")
        self.verify_button.config(state="normal")

    def erase_chip(self):
        if not self.device_detected:
            messagebox.showerror("Error", "Chip not detected. Please connect to the device first.")
            return
        try:
            self.programmer.erase()
            messagebox.showinfo("Success", "Chip erased successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def flash_firmware(self):
        if not self.device_detected:
            messagebox.showerror("Error", "Chip not detected. Please connect to the device first.")
            return
        filename = filedialog.askopenfilename(title="Select Firmware File", filetypes=[("Binary files", "*.bin")])
        if filename:
            try:
                self.programmer.erase()
                self.programmer.detect()
                bytes_written = self.programmer.flash_bin(filename)
                messagebox.showinfo("Success", f"{bytes_written} bytes flashed successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def verify_firmware(self):
        if not self.device_detected:
            messagebox.showerror("Error", "Chip not detected. Please connect to the device first.")
            return
        filename = filedialog.askopenfilename(title="Select Firmware File", filetypes=[("Binary files", "*.bin")])
        if filename:
            try:
                self.programmer.erase()
                self.programmer.detect()
                bytes_verified = self.programmer.verify_bin(filename)
                messagebox.showinfo("Success", f"{bytes_verified} bytes verified successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def exit_program(self):
        if self.programmer:
            try:
                self.programmer.exit()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.destroy()

    def run_programmer_exit(self):
        if self.programmer:
            try:
                self.programmer.exit()
                messagebox.showinfo("Success", "Programmer exit code executed successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No programmer instance found")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
