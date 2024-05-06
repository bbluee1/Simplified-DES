# Enkripsi dan Dekripsi S-DES

Repository ini berisi skrip Python untuk melakukan enkripsi dan dekripsi S-DES menggunakan antarmuka pengguna grafis (GUI) yang dibangun dengan Tkinter. S-DES (Simplified Data Encryption Standard) adalah versi yang disederhanakan dari algoritma Data Encryption Standard (DES). S-DES (Simplified Data Encryption Standard) Education merupakan skrip yang dikembangkan untuk pembelajaran proses enkripsi dan dekripsi menggunakan S-DES.

## Isi

1. [Pendahuluan](#pendahuluan)
2. [Ketergantungan](#ketergantungan)
3. [Penggunaan](#penggunaan)

## Pendahuluan

AES (Advanced Encryption Standard) adalah sebuah algoritma enkripsi kunci simetris yang digunakan secara luas untuk mengamankan data dalam berbagai aplikasi keamanan komputer. AES telah digunakan secara internasional sebagai pengganti algoritma DES (Data Encryption Standard) yang lebih lama. AES mendukung kunci enkripsi dengan panjang 128 bit, 192 bit, atau 256 bit. 
AES mengenkripsi data dalam blok-blok berukuran tetap, di mana panjang blok pesan adalah 128 bit. Pesan yang lebih panjang dibagi menjadi blok-blok 128 bit dan dienkripsi secara terpisah. AES menggunakan serangkaian putaran enkripsi, yang jumlahnya tergantung pada panjang kunci. Pada setiap putaran, data diubah menggunakan subkunci yang dihasilkan dari kunci utama. Operasi-operasi yang melibatkan substitusi, permutasi, dan XOR digunakan pada setiap putaran.
Sebelum putaran pertama dan setelah putaran terakhir, terjadi inisialisasi awal (initial permutation) dan permutasi akhir (final permutation) pada blok pesan. Inisialisasi awal mengatur data awal ke dalam urutan tertentu, sedangkan permutasi akhir mengubahnya kembali ke urutan aslinya. AES dianggap sangat aman dan tahan terhadap serangan-serangan modern, bahkan dengan panjang kunci yang lebih pendek (128 bit).

## Ketergantungan

Library Python berikut diperlukan untuk menjalankan skrip:
- `tkinter`: Digunakan untuk membangun antarmuka pengguna grafis (GUI).
- `pyperclip`: Digunakan untuk menyalin hasil ke clipboard.
- `webbrowser`: Digunakan untuk membuka tautan alamat email.

## Penggunaan

### Enkripsi dan Dekripsi

Untuk melakukan Enkripsi dan Dekripsi S-DES, ikuti langkah-langkah berikut:

1. Jalankan skrip `DES.py atau sesuai versi`.
2. Masukkan plaintext 8 bit atau ciphertext 8 bit dalam kolom input "Plaintext/ciphertext (8 bit)".
3. Masukkan kunci 10 bit dalam kolom input "Kunci (10 bit)".
4. Klik tombol "Encrypt" atau "Decrypt" untuk melakukan enkripsi/dekripsi.
5. Ciphertext/plaintext akan ditampilkan dalam area hasil.
6. Anda dapat mengklik tombol "Salin Hasil" untuk menyalin ciphertext/plaintext ke clipboard.
7. Klik reset untuk mengapus input dan output secara cepat

### - Contoh Input dan Output
  ```bash
  Plaintext:   00000001
  Key:         1001011000
  Ciphertext:  01101010
   ```
