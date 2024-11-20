#  Import Modul

import sqlite3 
#  Mengimpor modul sqlite3 yang digunakan untuk berinteraksi dengan database SQLite.

from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk 
# Mengimpor berbagai komponen dari modul tkinter yang akan digunakan untuk membuat antarmuka pengguna (GUI).

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') 
    # Membuat koneksi ke database SQLite dengan nama nilai_siswa.db.
    cursor = conn.cursor()
    #  Membuat sebuah cursor yang digunakan untuk mengeksekusi perintah SQL.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    # Mengeksekusi perintah SQL untuk membuat tabel nilai_siswa. Perintah CREATE TABLE IF NOT EXISTS akan membuat tabel hanya jika tabel belum ada.
    conn.commit()
    # Menyimpan perubahan ke database.
    conn.close()
    # Menutup koneksi ke database.

# Mengambil semua data dari tabel nilai_siswa dan mengembalikannya dalam bentuk list of tuples.
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    # Membuat koneksi ke database nilai_siswa.db.
    cursor = conn.cursor()
    # Membuat cursor untuk mengeksekusi perintah SQL.
    cursor.execute("SELECT * FROM nilai_siswa")
    # Mengeksekusi perintah SELECT * FROM nilai_siswa untuk mengambil semua data dari tabel.
    rows = cursor.fetchall()
    # Menyimpan hasil query ke dalam variabel rows.
    conn.close()
    # Menutup koneksi ke database.
    return rows
    # Mengembalikan rows yang berisi semua data siswa.

# Menyimpan data baru siswa ke dalam database.
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    # Membuat koneksi ke database.
    cursor = conn.cursor()
    # Membuat cursor.
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    # Mengeksekusi perintah INSERT untuk menambahkan data baru ke tabel. Parameter ? berfungsi sebagai placeholder untuk nilai yang akan disuntikkan ke dalam query.
    conn.commit() 
    # Menyimpan perubahan ke database.
    conn.close()
    # Menutup koneksi.

# Memperbarui data siswa yang sudah ada.
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    # Membuat koneksi ke database.
    cursor = conn.cursor()
    # Membuat cursor.
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    # Mengeksekusi perintah UPDATE untuk mengubah data pada baris yang sesuai dengan record_id.
    conn.commit()
    # Menyimpan perubahan ke database.
    conn.close()
    # Menutup koneksi.

# Menghapus data siswa berdasarkan ID.
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    # Membuat koneksi ke database.
    cursor = conn.cursor()
    # Membuat cursor.
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    # Mengeksekusi perintah DELETE untuk menghapus baris dengan id yang sesuai.
    conn.commit()
    # Menyimpan perubahan ke database.
    conn.close()
    # Menutup koneksi.

# Berfungsi untuk memprediksi fakultas yang cocok untuk seorang siswa berdasarkan nilai tiga mata pelajarannya (Biologi, Fisika, dan Inggris).
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran" 
        # Jika nilai Biologi adalah yang tertinggi.
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
        # Jika nilai Fisika adalah yang tertinggi.
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
        # Jika nilai Inggris adalah yang tertinggi.
    else:
        return "Tidak Diketahui"
        # Jika tidak ada nilai yang dominan.

# Fungsi ini digunakan untuk menyimpan data siswa baru ke dalam database.
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        # Mengambil nilai nama, nilai tiga mata pelajaran dari input pengguna.

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")
        # Memastikan nama siswa tidak kosong.

        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Memanggil fungsi calculate_prediction untuk mendapatkan prediksi fakultas.
        save_to_database(nama, biologi, fisika, inggris, prediksi)
        # Menyimpan data siswa (termasuk prediksi) ke dalam database menggunakan fungsi save_to_database.

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        # Memberikan pesan konfirmasi bahwa data berhasil disimpan.
        clear_inputs()
        # Mengosongkan form input.
        populate_table()
        # Memperbarui tampilan tabel dengan data terbaru.
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")
        # mengantisipasi kesalahan yang mungkin terjadi dan memberikan pesan yang jelas kepada pengguna, sehingga program dapat terus berjalan dengan lancar.

# Fungsi ini digunakan untuk memperbarui data siswa yang sudah ada.
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi ini digunakan untuk menghapus data siswa dari database.
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")
        # Memastikan pengguna telah memilih data yang ingin dihapus.

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        # Menghapus data siswa berdasarkan ID yang dipilih menggunakan fungsi delete_database.
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
        # Memperbarui tampilan tabel untuk menghilangkan data yang sudah dihapus.
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi ini digunakan untuk membersihkan atau mengosongkan semua field input dalam form.
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")
    # Setiap variabel yang terkait dengan field input (nama_var, biologi_var, fisika_var, inggris_var, dan selected_record_id) di-set menjadi string kosong.
    # Setelah variabel dikosongkan, form input pada GUI akan secara otomatis terbarui, menampilkan field-field kosong.

# Fungsi ini bertanggung jawab untuk mengisi tabel dengan data yang diambil dari database.
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
        # Menghapus semua baris data yang sudah ada dalam tabel.
    for row in fetch_data():
        # Memanggil fungsi fetch_data() untuk mengambil data terbaru dari database.
        tree.insert('', 'end', values=row)
        # Menambahkan setiap baris data yang diambil dari database ke dalam tabel.

# Fungsi ini digunakan untuk mengisi form input dengan data yang dipilih dari tabel.
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        #  Mengambil data dari baris yang dipilih dalam tabel.
        selected_row = tree.item(selected_item)['values']
        # Mengisi variabel yang terkait dengan field input dengan data yang diambil dari baris yang dipilih.

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
        # Setelah variabel diisi, form input akan secara otomatis terbarui, menampilkan data yang dipilih.
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")
        # Jika tidak ada data yang dipilih, akan muncul pesan error.

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
# Membuat sebuah label dengan teks "Nama Siswa".  Menempatkan label ini pada baris ke-0, kolom ke-0 dalam grid. Parameter padx dan pady digunakan untuk menambahkan jarak antara label dengan elemen di sekitarnya.
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)
# embuat sebuah entry field yang terhubung dengan variabel nama_var. Menempatkan entry field ini pada baris ke-0, kolom ke-1 dalam grid.

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
# Membuat sebuah label dengan teks "Nilai Biologi".  Menempatkan label ini pada baris ke-0, kolom ke-0 dalam grid. Parameter padx dan pady digunakan untuk menambahkan jarak antara label dengan elemen di sekitarnya.
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)
# embuat sebuah entry field yang terhubung dengan variabel biologi_var. Menempatkan entry field ini pada baris ke-0, kolom ke-1 dalam grid.

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
# Membuat sebuah label dengan teks "Nilai Fisika".  Menempatkan label ini pada baris ke-0, kolom ke-0 dalam grid. Parameter padx dan pady digunakan untuk menambahkan jarak antara label dengan elemen di sekitarnya.
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)
# embuat sebuah entry field yang terhubung dengan variabel fisika_var. Menempatkan entry field ini pada baris ke-0, kolom ke-1 dalam grid.

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
# Membuat sebuah label dengan teks "Nilai Inggris".  Menempatkan label ini pada baris ke-0, kolom ke-0 dalam grid. Parameter padx dan pady digunakan untuk menambahkan jarak antara label dengan elemen di sekitarnya.
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)
# embuat sebuah entry field yang terhubung dengan variabel inggris_var. Menempatkan entry field ini pada baris ke-0, kolom ke-1 dalam grid.

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
# Membuat sebuah tombol dengan teks "Add". Ketika tombol ini diklik, fungsi submit() akan dijalankan.
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
# Membuat sebuah tombol dengan teks "Update". Ketika tombol ini diklik, fungsi update() akan dijalankan.
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)
# Membuat sebuah tombol dengan teks "Delete". Ketika tombol ini diklik, fungsi delete() akan dijalankan.

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
# Membuat sebuah tuple yang berisi nama-nama kolom yang akan ditampilkan dalam tabel. Ini akan menjadi header kolom dalam tabel.
tree = ttk.Treeview(root, columns=columns, show='headings')
# Membuat objek

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
# Menempatkan tabel pada baris ke-5, kolom ke-0, dan melebarkannya hingga 3 kolom. 

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)
# Mengikat event klik kiri mouse pada tabel dengan fungsi fill_inputs_from_table.

populate_table()
# Memanggil fungsi populate_table() untuk mengisi tabel dengan data dari database.

root.mainloop()
# Memulai loop utama Tkinter untuk menampilkan jendela aplikasi dan merespons event pengguna.