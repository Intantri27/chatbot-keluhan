from flask import Flask, request, jsonify, render_template
import joblib
import re
import string

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


# Inisialisasi Flask
app = Flask(__name__)

# Load model dan vectorizer
model = joblib.load('model_naive_bayes.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')

# Inisialisasi stemmer dan stopword
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

# Fungsi preprocessing
def preprocessing_input(teks):
    teks = teks.lower()
    teks = re.sub(r'\d+', '', teks)
    teks = teks.translate(str.maketrans('', '', string.punctuation))
    teks = re.sub(r'\s+', ' ', teks).strip()
    teks = stopword_remover.remove(teks)
    teks = stemmer.stem(teks)
    return teks

# Respon otomatis per kategori
respon_kategori = {
    'Jaringan': 'Keluhan jaringan internet kamu telah kami terima. Tim IT kampus akan segera menindaklanjuti.',
    'Kebersihan': 'Keluhan kebersihan kamu telah kami terima. Petugas kebersihan akan segera ditugaskan.',
    'Akademik': 'Keluhan akademik kamu telah kami terima. Pihak akademik akan segera menindaklanjuti.',
    'Administrasi': 'Keluhan administrasi kamu telah kami terima. Staf TU akan segera memproses keluhanmu.',
    'Fasilitas': 'Keluhan fasilitas kamu telah kami terima. Tim sarana prasarana akan segera menangani.'
}

# Route halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route API prediksi
@app.route('/prediksi', methods=['POST'])
def prediksi():
    data = request.get_json()
    teks = data.get('teks', '')

    if not teks:
        return jsonify({'error': 'Teks kosong'}), 400

    teks_bersih = preprocessing_input(teks)
    vektor = tfidf.transform([teks_bersih])
    kategori = model.predict(vektor)[0]
    respon = respon_kategori.get(kategori, 'Keluhan kamu telah kami terima.')

    return jsonify({
        'kategori': kategori,
        'respon': respon
    })

# Jalankan Flask
if __name__ == '__main__':
    app.run(debug=True)