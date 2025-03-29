import secrets
import string
import tkinter as tk
from tkinter import messagebox
import re

# Common Weak Passwords
COMMON_PASSWORDS = {"12345678", "password", "qwerty", "abc123", "letmein", "123456", "111111", "123123", "password1", "1234"}

class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("500x600")  # Set the window size big enough to fit all elements
        self.root.resizable(False, False)  # Keep window size fixed (non-resizable)

        # Default theme is light mode
        self.is_dark_mode = False

        # Initialize UI elements before setting the theme
        self.title_label = tk.Label(root, text="🔐 Password Manager", font=("Helvetica", 16, "bold"))
        self.generate_btn = tk.Button(root, text="Generate Password", command=self.generate_password, font=("Helvetica", 12), width=20, relief="flat", height=2)
        self.password_entry = tk.Entry(root, font=("Helvetica", 12), width=30, justify="center", relief="solid", bd=2)
        self.copy_btn = tk.Button(root, text="Copy", command=self.copy_password, width=20, relief="flat", height=2)
        self.check_label = tk.Label(root, text="🔍 Check Password Strength:", font=("Helvetica", 10))
        self.check_entry = tk.Entry(root, font=("Helvetica", 12), width=30, justify="center", relief="solid", bd=2)
        self.check_btn = tk.Button(root, text="Check Strength", command=self.check_strength, font=("Helvetica", 12), width=20, relief="flat", height=2)
        self.mode_button = tk.Button(root, text="Switch to Dark Mode", command=self.toggle_theme, font=("Helvetica", 12), width=20, relief="flat", height=2)

        # Set the theme after initializing all UI elements
        self.set_theme()

        # Pack all elements with proper padding for a clean layout
        self.title_label.pack(pady=30)
        self.generate_btn.pack(pady=10)
        self.password_entry.pack(pady=10)
        self.copy_btn.pack(pady=15)
        self.check_label.pack(pady=15)
        self.check_entry.pack(pady=10)
        self.check_btn.pack(pady=15)
        self.mode_button.pack(pady=20)

    def set_theme(self):
        """Sets the theme for light/dark mode."""
        if self.is_dark_mode:
            self.bg_color = "#333333"  # Dark background color
            self.fg_color = "#FFFFFF"  # White text
            self.button_bg = "#444444"  # Dark button background
            self.button_fg = "#FFFFFF"  # White text on buttons
            self.entry_bg = "#555555"  # Dark entry box background
            self.entry_fg = "#FFFFFF"  # White text in entry boxes
        else:
            self.bg_color = "#FFFFFF"  # Light background color
            self.fg_color = "#000000"  # Black text
            self.button_bg = "#DDDDDD"  # Light button background
            self.button_fg = "#000000"  # Black text on buttons
            self.entry_bg = "#FFFFFF"  # Light entry box background
            self.entry_fg = "#000000"  # Black text in entry boxes
        
        # Update the root window color
        self.root.config(bg=self.bg_color)

        # Update all components' colors after theme has been set
        self.title_label.config(bg=self.bg_color, fg=self.fg_color)
        self.check_label.config(bg=self.bg_color, fg=self.fg_color)
        self.generate_btn.config(bg=self.button_bg, fg=self.button_fg)
        self.copy_btn.config(bg=self.button_bg, fg=self.button_fg)
        self.check_btn.config(bg=self.button_bg, fg=self.button_fg)
        self.mode_button.config(bg=self.button_bg, fg=self.button_fg)
        self.password_entry.config(bg=self.entry_bg, fg=self.entry_fg)
        self.check_entry.config(bg=self.entry_bg, fg=self.entry_fg)

    def toggle_theme(self):
        """Toggles between light and dark mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.set_theme()
        mode_text = "Switch to Light Mode" if self.is_dark_mode else "Switch to Dark Mode"
        self.mode_button.config(text=mode_text)

    def generate_password(self):
        """Generates a secure password."""
        length = secrets.choice(range(12, 19))
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_password(self):
        """Copies password to clipboard."""
        password = self.password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    def check_strength(self):
        """Checks password strength."""
        password = self.check_entry.get()

        if password in COMMON_PASSWORDS:
            messagebox.showerror("Weak Password", "⚠️ This password is extremely common! Choose a stronger one.")
            return

        length_score = min(len(password) / 18, 1)
        variety_score = sum(bool(re.search(pattern, password)) for pattern in [
            r'[A-Z]', r'[a-z]', r'[0-9]', r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~]'
        ]) / 4

        score = (length_score * 0.5) + (variety_score * 0.5)

        if score < 0.4:
            messagebox.showwarning("Weak Password", "⚠️ Weak Password! Add uppercase, numbers, and special characters.")
        elif score < 0.7:
            messagebox.showinfo("Moderate Password", "🟡 Moderate Password! Try making it longer for better security.")
        else:
            messagebox.showinfo("Strong Password", "✅ Strong Password!")

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
