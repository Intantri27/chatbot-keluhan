import joblib
import re
import string

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Load model dan TF-IDF
model = joblib.load("model_naive_bayes.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

# Stemmer dan Stopword
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

# Respon otomatis
solusi_kategori = {

    "Jaringan": """
Berdasarkan hasil analisis, keluhan Anda termasuk dalam kategori Jaringan.

Silakan mencoba beberapa langkah berikut terlebih dahulu:

• Pastikan perangkat telah terhubung ke jaringan WiFi kampus yang benar.
• Matikan lalu aktifkan kembali koneksi WiFi.
• Restart perangkat apabila diperlukan.
• Coba berpindah ke access point lain apabila tersedia.

Apabila kendala masih terjadi, laporan Anda akan diteruskan kepada Tim Teknologi Informasi (IT) untuk dilakukan pemeriksaan lebih lanjut.

Terima kasih telah menggunakan CampusVoice.
""",

    "Akademik": """
Berdasarkan hasil analisis, keluhan Anda termasuk dalam kategori Akademik.

Silakan memastikan beberapa hal berikut:

• Jadwal perkuliahan atau jadwal input nilai telah sesuai.
• Data pada Sistem Informasi Akademik (SIAKAD) telah diperbarui.
• Informasi telah dikonfirmasi kepada dosen pengampu atau program studi apabila diperlukan.

Jika kendala belum terselesaikan, laporan Anda akan diteruskan kepada bagian akademik untuk ditindaklanjuti.

Terima kasih telah menggunakan CampusVoice.
""",

    "Administrasi": """
Berdasarkan hasil analisis, keluhan Anda termasuk dalam kategori Administrasi.

Silakan memastikan:

• Persyaratan administrasi telah dipenuhi.
• Dokumen atau formulir telah dikirim dengan benar.
• Estimasi waktu pelayanan telah terlewati.

Apabila kendala masih terjadi, laporan akan diteruskan kepada bagian administrasi untuk diproses lebih lanjut.

Terima kasih telah menggunakan CampusVoice.
""",

    "Fasilitas": """
Berdasarkan hasil analisis, keluhan Anda termasuk dalam kategori Fasilitas.

Sistem menyarankan agar Anda memastikan fasilitas telah digunakan sesuai prosedur.

Apabila kendala masih terjadi atau ditemukan kerusakan pada fasilitas kampus, laporan Anda akan diteruskan kepada Tim Sarana dan Prasarana agar dapat dilakukan pemeriksaan, perbaikan, maupun penggantian apabila diperlukan.

Terima kasih telah menggunakan CampusVoice.
""",

    "Kebersihan": """
Berdasarkan hasil analisis, keluhan Anda termasuk dalam kategori Kebersihan.

Laporan Anda akan diteruskan kepada petugas kebersihan kampus agar kondisi lingkungan dapat segera diperiksa dan ditangani.

Terima kasih telah menggunakan CampusVoice.
"""
}

# Preprocessing
def preprocessing_input(teks):
    teks = teks.lower()
    teks = re.sub(r'\d+', '', teks)
    teks = teks.translate(str.maketrans('', '', string.punctuation))
    teks = re.sub(r'\s+', ' ', teks).strip()
    teks = stopword_remover.remove(teks)
    teks = stemmer.stem(teks)
    return teks

# Prediksi
def prediksi_keluhan(teks):

    teks_bersih = preprocessing_input(teks)

    vektor = tfidf.transform([teks_bersih])

    kategori = model.predict(vektor)[0]

    solusi = solusi_kategori.get(
        kategori,
        "Keluhan berhasil diklasifikan."
    )

    return kategori, solusi