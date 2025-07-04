import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

# Function to generate a secure AES-256 key using Fernet and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Key Generated", "A new encryption key has been saved as 'secret.key'.")

# Function to load the previously saved key
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt a selected file using the AES-256 key
def encrypt_file():
    try:
        file_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if not file_path:
            return

        key = load_key()
        fernet = Fernet(key)

        with open(file_path, "rb") as file:
            original_data = file.read()

        encrypted_data = fernet.encrypt(original_data)

        with open(file_path + ".enc", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        messagebox.showinfo("Success", f"Encrypted file saved as:\n{file_path}.enc")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")

# Function to decrypt a selected .enc file using the AES-256 key
def decrypt_file():
    try:
        file_path = filedialog.askopenfilename(title="Select File to Decrypt")
        if not file_path:
            return

        key = load_key()
        fernet = Fernet(key)

        with open(file_path, "rb") as enc_file:
            encrypted_data = enc_file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        output_file = file_path.replace(".enc", "") + ".dec"
        with open(output_file, "wb") as dec_file:
            dec_file.write(decrypted_data)

        messagebox.showinfo("Success", f"Decrypted file saved as:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")

# GUI layout setup
app = tk.Tk()
app.title("AES-256 File Encryption Tool")
app.geometry("420x300")
app.resizable(False, False)

tk.Label(app, text="AES-256 File Encryption/Decryption", font=("Arial", 14)).pack(pady=20)
tk.Button(app, text="Generate Key", width=35, command=generate_key).pack(pady=10)
tk.Button(app, text="Encrypt File", width=35, command=encrypt_file).pack(pady=10)
tk.Button(app, text="Decrypt File", width=35, command=decrypt_file).pack(pady=10)

app.mainloop()