import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import json
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))


class function_from_rust:
    @staticmethod
    def encrypt_file_rust(input_path, output_path, key):
        try:
            result = subprocess.run(
                ["../rust_func/target/release/file_encryption.exe", "encrypt", input_path, output_path, key],
                check=True,
                text=True,
                capture_output=True
            )
            messagebox.showinfo("Success", "File successfully encrypted")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error: incorrect file path")

    @staticmethod
    def decrypt_file_rust(input_path, output_path, key):
        try:
            result = subprocess.run(
                ["../rust_func/target/release/file_encryption.exe", "decrypt", input_path, output_path, key],
                check=True,
                text=True,
                capture_output=True
            )
            messagebox.showinfo("Success", "File decrypted")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", "Error: incorrect encryption key")

    @staticmethod
    def generate_key_rust():
        try:
            result = subprocess.run(
                ["../rust_func/target/release/file_encryption.exe", "generate_key"],
                check=True,
                text=True,
                capture_output=True
            )
            key_entry.delete(0, tk.END)
            key_entry.insert(0, result.stdout.split(":")[1].strip()) 
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error creating encryption key")

def browse_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def save_file():
    filename = filedialog.asksaveasfilename(defaultextension=".enc")
    save_entry.delete(0, tk.END)
    save_entry.insert(0, filename)

def on_encrypt():
    input_path = file_entry.get()
    output_path = save_entry.get()
    key = key_entry.get()
    if input_path and output_path and key:
        function_from_rust.encrypt_file_rust(input_path, output_path, key)

def on_decrypt():
    input_path = file_entry.get()
    output_path = save_entry.get()
    key = key_entry.get()
    if input_path and output_path and key:
        function_from_rust.decrypt_file_rust(input_path, output_path, key)

def change_language(lang):
    with open("text.json", "r+", encoding="utf-8") as file:
        transl_dict = json.load(file)
        
        file_label.config(text=transl_dict[lang]["input_file"])
        save_label.config(text=transl_dict[lang]["output_file"])
        key_label.config(text=transl_dict[lang]["key_text"])
        generate_key_button.config(text=transl_dict[lang]["key_button"])
        encrypt_button.config(text=transl_dict[lang]["encrypt_button"])
        decrypt_button.config(text=transl_dict[lang]["decrypt_button"])
        instructions_text_var.set(transl_dict[lang]["instructions_text"]) 
        file_button.config(text=transl_dict[lang]["browse"])
        save_button.config(text=transl_dict[lang]["browse"])
        text_about_key.config(text=transl_dict[lang]["lost_key"])
        
        transl_dict["Language"] = lang

        file.seek(0)
        json.dump(transl_dict, file, ensure_ascii=False, indent=4)
        file.truncate()


# параметры основного окна
root = tk.Tk()
root.title("QuickCrypt")
root.geometry("1400x800")
root.config(background='#1e2129')
root.maxsize(1400, 800)
root.minsize(1400, 800)
root.columnconfigure(0, weight=0, minsize=400)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=0) 
root.rowconfigure(1, weight=0) 
root.rowconfigure(2, weight=1)  
root.rowconfigure(3, weight=0)  


# параметры для первого файла
row_for_first_file = tk.Frame(root, background='#1e2129')
row_for_first_file.grid(row=0, column=0, sticky="ew", padx=10, pady=20)  

file_label = tk.Label(row_for_first_file, text="File for encryption/decryption:", font='Nova 16', fg='white', background='#1e2129')
file_label.grid(row=0, column=0, sticky="we", padx=5, pady=15)

file_entry = tk.Entry(row_for_first_file, width=50, font=("Nova", 16))
file_entry.grid(row=1, column=0, padx=5)

file_button = tk.Button(row_for_first_file, text="Browse", command=browse_file, height=2, width=20, background='#1878af', fg='white', font=("Nova", 16))
file_button.grid(row=2, column=0, padx=5, pady=15)

# параметры для второго файла
row_for_second_file = tk.Frame(root, background='#1e2129')
row_for_second_file.grid(row=1, column=0, sticky="ew", padx=5, pady=15)

save_label = tk.Label(row_for_second_file, text="File for saving:", font='Nova 16', fg='white', background='#1e2129')
save_label.grid(row=0, column=0, sticky="we", padx=5, pady=15)

save_entry = tk.Entry(row_for_second_file, width=50, font=("Nova", 16))
save_entry.grid(row=1, column=0, padx=5)

save_button = tk.Button(row_for_second_file, text="Browse", command=save_file, height=2, width=20, background='#1878af', fg='white', font=("Nova", 16))
save_button.grid(row=2, column=0, padx=5, pady=15)

# параметры для ключа
row_for_key = tk.Frame(root, background='#1e2129')
row_for_key.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

key_label = tk.Label(row_for_key, text="Encryption Key:", font='Nova 16', fg='white', background='#1e2129')
key_label.grid(row=0, column=0, sticky="we", padx=5, pady=15)

key_entry = tk.Entry(row_for_key, width=50, font=("Nova", 16))
key_entry.grid(row=1, column=0, padx=5)

generate_key_button = tk.Button(row_for_key, text="Generate Key", command=function_from_rust.generate_key_rust, height=2, width=20, background='#1878af', fg='white', font=("Nova", 16))
generate_key_button.grid(row=2, column=0, padx=5, pady=15)

text_about_key = tk.Label(row_for_key, text="IF YOU LOSE THE KEY, YOU WILL NO LONGER BE ABLE TO DECRYPT THE FILE", font='Nova 11', fg='white', background='#1e2129')
text_about_key.grid(row=3, column=0, padx=5, pady=15)

# параметры для текста инструкций
row_for_instructions_text = tk.Frame(root, background='#1e2129')
row_for_instructions_text.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
instructions_text_var = tk.StringVar()
instructions_text_var.set("1) Click \"Browse\" in the \"File for encryption/decryption\" section to select the input file.\n2) Specify the output file by clicking \"Browse\" in the \"File for saving\" section.\n3) Enter the key manually or click \"Generate Key\".\n4) Click \"Encrypt\" to encrypt the file or \"Decrypt\" to decrypt it.\n5) Use the correct key; otherwise, the file cannot be decrypted.")
instructions_text = tk.Label(
    row_for_instructions_text, 
    textvariable=instructions_text_var,  
    font='Nova 12', 
    fg='white', 
    background='#1e2129', 
    anchor="center", 
    justify="center",  
    wraplength=1100
)
instructions_text.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
row_for_instructions_text.grid_rowconfigure(0, weight=1) 
row_for_instructions_text.grid_columnconfigure(0, weight=1)  

# параметры для кнопок Encrypt и Decrypt
row_for_buttons = tk.Frame(root, background='#1e2129')
row_for_buttons.grid(row=2, column=1, sticky="ew", padx=250, pady=5)

encrypt_button = tk.Button(row_for_buttons, text="Encrypt", command=on_encrypt, height=2, width=20, background='#1878af', fg='white', font=("Nova", 16))
encrypt_button.grid(row=0, column=0, padx=5, pady=5)

decrypt_button = tk.Button(row_for_buttons, text="Decrypt", command=on_decrypt, height=2, width=20, background='#1878af', fg='white', font=("Nova", 16))
decrypt_button.grid(row=1, column=0, padx=5, pady=50)

# параметры для выбора языка
row_for_language = tk.Frame(root, background='#1e2129')
row_for_language.grid(row=3, column=1, sticky="se", padx=10, pady=5)

button_russia = tk.Button(row_for_language, text="RU", height=1, width=3, background='#1878af', fg='white', command=lambda: change_language('Russia'), font=("Nova", 16))
button_russia.grid(row=0, column=0, padx=5, pady=5)

button_english = tk.Button(row_for_language, text="EN", height=1, width=3, background='#1878af', fg='white', command=lambda: change_language('English'), font=("Nova", 16))
button_english.grid(row=0, column=1, padx=5, pady=5)


with open("text.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    change_language(data["Language"])


root.mainloop()