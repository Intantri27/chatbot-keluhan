import sqlite3

DATABASE = "database.db"
def get_connection():
    conn = sqlite3.connect(DATABASE)
    # hasil query bisa dipanggil berdasarkan nama kolom
    conn.row_factory = sqlite3.Row
    return conn

# Membuat tabel
def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Tabel Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        nim TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Tabel Keluhan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keluhan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nim TEXT NOT NULL,
        isi_keluhan TEXT NOT NULL,
        kategori TEXT NOT NULL,
        status TEXT DEFAULT 'Menunggu',
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (nim)
        REFERENCES users(nim)
    )
    """)

    conn.commit()
    conn.close()

# Menambahkan akun default
def insert_default_users():

    conn = get_connection()
    cursor = conn.cursor()

    # Admin
    cursor.execute("""

    INSERT OR IGNORE INTO users
    (nama,nim,username,password,role)

    VALUES
    (?,?,?,?,?)

    """,

    (
        "Administrator",
        None,
        "admin",
        "admin123",
        "admin"
    ))

    # Mahasiswa
    cursor.execute("""

    INSERT OR IGNORE INTO users
    (nama,nim,username,password,role)

    VALUES
    (?,?,?,?,?)

    """,

    (
        "Intan Tri Hartati",
        "24090039",
        None,
        "123456",
        "mahasiswa"
    ),
    (
        "Arthala Aruna",
        "24090040",
        None,
        "123456",
        "mahasiswa"
    ),
    (
        "Taksa Denandra",
        "24090098",
        None,
        "123456",
        "mahasiswa"
    ))

    conn.commit()
    conn.close()

# Login
def login_user(identifier, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM users
    WHERE (nim=? OR username=?) AND password=?

    """,
    (
        identifier,
        identifier,
        password
    ))

    user = cursor.fetchone()
    conn.close()
    return user

# Simpan Keluhan
def simpan_keluhan(nim, isi_keluhan, kategori):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO keluhan
    (nim,isi_keluhan,kategori) VALUES (?,?,?)
    """,
    (
        nim,
        isi_keluhan,
        kategori
    ))
    conn.commit()
    conn.close()

# Riwayat Keluhan Mahasiswa
def get_keluhan_mahasiswa(nim):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM keluhan WHERE nim=? ORDER BY tanggal DESC """,

    (nim,))
    data = cursor.fetchall()
    conn.close()
    return data

# Semua Keluhan (Admin)
def get_semua_keluhan():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM keluhan ORDER BY tanggal DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

# Dashboard Admin
def get_dashboard_admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM keluhan")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM keluhan WHERE status='Menunggu'")
    menunggu = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM keluhan WHERE status='Diproses'")
    diproses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM keluhan WHERE status='Selesai'")
    selesai = cursor.fetchone()[0]

    conn.close()

    return {

        "total": total,
        "menunggu": menunggu,
        "diproses": diproses,
        "selesai": selesai

    }

# Keluhan Terbaru
def get_keluhan_terbaru():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM keluhan
        ORDER BY tanggal DESC LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data



# Update Status Keluhan
def update_status(id_keluhan, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE keluhan SET status=? WHERE id=?
    """,
    (
        status,
        id_keluhan
    ))

    conn.commit()
    conn.close()

# Main
if __name__ == "__main__":

    create_tables()
    insert_default_users()
    print("Database berhasil dibuat.")