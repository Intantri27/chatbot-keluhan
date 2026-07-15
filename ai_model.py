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

    "Jaringan":
"""
Saya mendeteksi keluhan Anda berkaitan dengan jaringan internet.

Sebelum laporan dikirim, silakan coba beberapa langkah berikut:

• Pastikan perangkat terhubung ke WiFi kampus yang benar.
• Matikan lalu hidupkan kembali koneksi WiFi.
• Coba berpindah ke access point lain.
• Restart perangkat apabila diperlukan.

Jika masalah masih terjadi, Anda dapat mengirim laporan kepada pihak kampus.
""",

    "Akademik":
"""
Saya mendeteksi keluhan Anda berkaitan dengan akademik.

Silakan pastikan:

• Jadwal input nilai telah selesai.
• Anda sudah login ulang ke SIAKAD.
• Hubungi dosen pengampu apabila diperlukan.

Jika masalah belum terselesaikan, silakan kirim laporan.
""",

    "Administrasi":
"""
Saya mendeteksi keluhan administrasi.

Silakan memastikan:

• Persyaratan administrasi telah lengkap.
• Formulir sudah dikirim.
• Estimasi waktu pelayanan telah terlewati.

Jika masih mengalami kendala, silakan kirim laporan.
""",

    "Fasilitas":
"""
Saya mendeteksi keluhan fasilitas.

Silakan coba:

• Pastikan perangkat sudah dinyalakan.
• Periksa kabel daya.
• Periksa kabel HDMI/VGA apabila menggunakan proyektor.

Jika masih bermasalah, silakan kirim laporan.
""",

    "Kebersihan":
"""
Saya mendeteksi keluhan mengenai kebersihan.

Apabila kondisi tersebut masih terjadi, laporan akan diteruskan kepada petugas kebersihan kampus.
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