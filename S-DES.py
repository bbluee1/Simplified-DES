import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip  # Untuk meng-copy hasil ke clipboard

# Inisialisasi tabel substitusi dan permutasi
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]
S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

# Helper function untuk melakukan permutasi
def permute(input_text, permutation_table):
    return ''.join(input_text[i - 1] for i in permutation_table)

# Helper function untuk melakukan left shift pada string
def left_shift(input_text, shifts):
    return input_text[shifts:] + input_text[:shifts]

# Fungsi untuk menghasilkan subkeys
def generate_subkeys(key):
    key = permute(key, P10)
    key_left = key[:5]
    key_right = key[5:]
    key_left_shifted = left_shift(key_left, 1)
    key_right_shifted = left_shift(key_right, 1)
    subkey1 = permute(key_left_shifted + key_right_shifted, P8)

    key_left_shifted = left_shift(key_left_shifted, 2)
    key_right_shifted = left_shift(key_right_shifted, 2)
    subkey2 = permute(key_left_shifted + key_right_shifted, P8)

    return subkey1, subkey2

# Fungsi untuk melakukan F-function pada input_text dan subkey
def f_function(input_text, subkey):
    input_text = permute(input_text, EP)
    xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(input_text, subkey))
    left_half = xor_result[:4]
    right_half = xor_result[4:]
    row1 = int(left_half[0] + left_half[3], 2)
    col1 = int(left_half[1] + left_half[2], 2)
    row2 = int(right_half[0] + right_half[3], 2)
    col2 = int(right_half[1] + right_half[2], 2)
    s0_value = S0[row1][col1]
    s1_value = S1[row2][col2]
    s_result = bin(s0_value)[2:].zfill(2) + bin(s1_value)[2:].zfill(2)
    p4_result = permute(s_result, P4)
    return p4_result

# Fungsi S-DES Encryption
def sdes_encrypt(plaintext, key):
    # Initial Permutation (IP)
    plaintext = permute(plaintext, IP)

    # Generate Subkeys
    subkey1, subkey2 = generate_subkeys(key)

    # Round 1
    left_half = plaintext[:4]
    right_half = plaintext[4:]

    # F-function pertama dengan subkey1
    f_result = f_function(right_half, subkey1)

    # XOR hasil F-function dengan left_half
    xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(left_half, f_result))

    # Pertukaran left_half dan right_half
    left_half, right_half = right_half, xor_result

    # Round 2
    # F-function kedua dengan subkey2
    f_result = f_function(right_half, subkey2)

    # XOR hasil F-function dengan left_half
    xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(left_half, f_result))

    # Final Permutation (IP^-1)
    ciphertext = xor_result + right_half
    ciphertext = permute(ciphertext, IP_INV)

    return ciphertext

# Fungsi S-DES Decryption
def sdes_decrypt(ciphertext, key):
    # Initial Permutation (IP)
    ciphertext = permute(ciphertext, IP)

    # Generate Subkeys
    subkey1, subkey2 = generate_subkeys(key)

    # Round 1
    left_half = ciphertext[:4]
    right_half = ciphertext[4:]

    # F-function pertama dengan subkey2 (beda dari enkripsi)
    f_result = f_function(right_half, subkey2)

    # XOR hasil F-function dengan left_half
    xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(left_half, f_result))

    # Pertukaran left_half dan right_half
    left_half, right_half = right_half, xor_result

    # Round 2
    # F-function kedua dengan subkey1 (beda dari enkripsi)
    f_result = f_function(right_half, subkey1)

    # XOR hasil F-function dengan left_half
    xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(left_half, f_result))

    # Final Permutation (IP^-1)
    plaintext = xor_result + right_half
    plaintext = permute(plaintext, IP_INV)

    return plaintext

# Fungsi untuk mengenkripsi atau mendekripsi saat tombol "Encrypt" atau "Decrypt" diklik
def process_button_clicked(encrypt=True):
    global encryption_done  # Gunakan variabel global encryption_done

    # Menonaktifkan tombol "Salin" saat proses sedang berlangsung
    copy_button.config(state="disabled")

    plaintext = input_entry.get()
    key = key_entry.get()

    # Periksa apakah input adalah angka biner (hanya mengandung 0 dan 1)
    if not (plaintext.isdigit() and all(char in '01' for char in plaintext)) or \
       not (key.isdigit() and all(char in '01' for char in key)):
        messagebox.showerror("Error", "Input harus berupa angka biner (hanya mengandung 0 dan 1)")
        return

    # Periksa panjang plaintext dan kunci
    if len(plaintext) != 8:
        messagebox.showerror("Error", "Plaintext/Ciphertext harus 8 bit biner")
        return

    if len(key) != 10:
        messagebox.showerror("Error", "Kunci harus 10 bit biner")
        return

    # Padding plaintext jika kurang dari 8 bit
    if len(plaintext) < 8:
        plaintext = plaintext.zfill(8)

    # Lakukan enkripsi atau dekripsi menggunakan S-DES tergantung pada argumen "encrypt"
    if encrypt:
        ciphertext = sdes_encrypt(plaintext, key)
        result_label.config(
            text="Ciphertext: " + ciphertext,
            foreground="red",
            font=("Arial", 10, "bold"),
            justify="center",
            anchor="center"
        )
        
        # Mengaktifkan tombol "Salin" saat enkripsi dilakukan
        copy_button.config(state="normal")
    else:
        plaintext = sdes_decrypt(plaintext, key)
        result_label.config(
            text="Plaintext: " + plaintext,
            foreground="blue",
            font=("Arial", 10, "bold"),
            justify="center",
            anchor="center"
        )
        
        # Mengaktifkan tombol "Salin" saat dekripsi dilakukan
        copy_button.config(state="normal")
        encryption_done = True  # Mengatur encryption_done menjadi True setelah dekripsi selesai

# Fungsi untuk menyalin hasil ke clipboard
def copy_button_clicked():
    result = result_label.cget("text")
    result = result.split(": ")[1]  # Mengambil bagian setelah ": "
    pyperclip.copy(result)
    
    # Menampilkan notifikasi
    messagebox.showinfo("Sukses", "Hasil berhasil disalin ke clipboard.")

# Fungsi untuk mereset input dan output
def reset_fields():
    global encryption_done  # Gunakan variabel global encryption_done

    # Menonaktifkan tombol "Salin"
    copy_button.config(state="disabled")
    
    # Menghapus konten dari elemen input, kunci, dan output heksadesimal
    input_entry.delete(0, tk.END)
    key_entry.delete(0, tk.END)
    
    # Mengosongkan teks biner output
    result_label.config(text="😊")

# Fungsi untuk mengatur jendela di tengah layar
def center_window(window, width, height):
    # Mendapatkan lebar dan tinggi layar
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Menghitung posisi x dan y untuk menempatkan jendela di tengah layar
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Mengatur geometri jendela sesuai dengan posisi dan ukuran yang telah dihitung
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)  # Menonaktifkan kemampuan untuk merubah ukuran jendela

# Membuat jendela tkinter
window = tk.Tk()
window.title("Simplified DES")
window.configure(bg="#2596be")  # Mengatur warna latar belakang jendela utama

# Mengatur ukuran jendela
window_width = 320
window_height = 350

# Variabel global
encryption_done = False  # Inisialisasi variabel encryption_done

# Menyimpan jendela di tengah layar
center_window(window, window_width, window_height)

# Menggunakan tema modern
style = ttk.Style()
style.theme_use("clam")

# Versi aplikasi
app_version = "1.0"

# Mengambil teks judul dari jendela
judul_jendela = window.title()

# Label judul dengan font yang lebih besar dan warna teks
title_label = ttk.Label(window, text=judul_jendela, font=("Helvetica", 18, "bold"), background=window.cget('bg'))
title_label.pack(pady=(20, 5))  # Padding atas 20, bawah 5

# Label versi dengan font yang lebih kecil
version_label = ttk.Label(window, text=f"Versi {app_version}", font=("Helvetica", 10), background=window.cget('bg'))
version_label.pack()

# Agar label versi berada di bawah label judul
title_label.pack(pady=(20, 0))

# Membuat frame utama
main_frame = ttk.Frame(window, padding=1)
main_frame.place(relx=1, rely=1, anchor=tk.CENTER)

# Mengatur perilaku frame
main_frame.pack(fill=tk.BOTH, expand=False)
main_frame['style'] = 'My.TFrame'

# Membuat label untuk plaintext/ciphertext
text_label = ttk.Label(main_frame, text="Plaintext/Ciphertext (8 bit):", anchor="center")
text_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Membuat entri input untuk plaintext/ciphertext
input_entry = ttk.Entry(main_frame, justify="right")
input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

# Membuat label untuk kunci (10 bit)
key_label = ttk.Label(main_frame, text="Kunci (10 bit):", anchor="center")
key_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Membuat entri input untuk kunci (10 bit)
key_entry = ttk.Entry(main_frame, justify="right")
key_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")

# Membuat frame untuk tombol-tombol
button_frame = ttk.Frame(main_frame, padding=5)
button_frame.grid(row=3, column=0, columnspan=3, pady=10)

# Membuat tombol Reset
reset_button = ttk.Button(button_frame, text="Reset", command=reset_fields, width=10)
reset_button.grid(row=3, column=0, padx=(10, 5), pady=10)

# Membuat tombol Decrypt
decrypt_button = ttk.Button(button_frame, text="Decrypt", command=lambda: process_button_clicked(False), width=10)
decrypt_button.grid(row=3, column=1, padx=5, pady=10)

# Membuat tombol Encrypt
encrypt_button = ttk.Button(button_frame, text="Encrypt", command=lambda: process_button_clicked(True), width=10)
encrypt_button.grid(row=3, column=2, padx=(5, 10), pady=10)

# Membuat label hasil awal dengan font yang lebih besar dan warna teks
result_label = ttk.Label(main_frame, text="", font=("Arial", 14, "bold"), foreground="darkblue")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10))

# Membuat tombol Copy Hasil
copy_button = ttk.Button(main_frame, text="Copy Hasil", command=copy_button_clicked)
copy_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 10))
copy_button.config(state="disabled")  # Menonaktifkan tombol saat pertama kali dijalankan

# Membuat label hak cipta
copyright_label = ttk.Label(main_frame, text="© 2024", font=("Helvetica", 8, "bold"), foreground="grey", cursor="hand2")
copyright_label.grid(row=6, column=0, columnspan=2, pady=(0, 10))
copyright_label.configure(anchor="center", justify="center")

def open_email(event):
    import webbrowser
    webbrowser.open("mailto:imamsyt22@mhs.usk.ac.id")

# Menghubungkan fungsi dengan klik pada teks hak cipta
copyright_label.bind("<Button-1>", open_email)

window.mainloop()
