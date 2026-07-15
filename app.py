from flask import Flask, request, jsonify, render_template, redirect, session
from database import (login_user, simpan_keluhan, get_keluhan_mahasiswa, get_semua_keluhan, update_status)

from ai_model import prediksi_keluhan

app = Flask(__name__)
app.secret_key = "campusvoice"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        identifier = request.form["identifier"]
        password = request.form["password"]

        user = login_user(identifier, password)

        if user:

            session["nama"] = user["nama"]
            session["role"] = user["role"]
            session["nim"] = user["nim"]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="NIM/Username atau Password salah."
        )

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "role" not in session:
        return redirect("/login")

    if session["role"] == "admin":
        return render_template(
            "dashboard_admin.html",
            nama=session["nama"]
        )

    return render_template(
        "dashboard_mhs.html",
        nama=session["nama"]
    )

@app.route("/riwayat")
def riwayat():

    if "nim" not in session:
        return redirect("/login")

    data_keluhan = get_keluhan_mahasiswa(session["nim"])

    return render_template(
        "riwayat.html",
        data=data_keluhan
    )

@app.route("/kelola_keluhan")
def kelola_keluhan():

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/dashboard")

    data = get_semua_keluhan()

    return render_template(
        "kelola_keluhan.html",
        data=data
    )

@app.route("/update_status/<int:id>", methods=["POST"])
def ubah_status(id):

    if "role" not in session:
        return redirect("/login")

    status = request.form["status"]

    update_status(id, status)

    return redirect("/kelola_keluhan")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/prediksi", methods=["POST"])
def prediksi():

    data = request.get_json()
    teks = data.get("teks", "")
    if not teks:
        return jsonify({
            "error": "Teks kosong"
        }), 400
    kategori, solusi = prediksi_keluhan(teks)

    return jsonify({
        "kategori": kategori,
        "respon": solusi
    })

@app.route("/simpan_keluhan", methods=["POST"])
def kirim_keluhan():
    if "nim" not in session:
        return jsonify({
            "error": "Anda harus login terlebih dahulu."
        }), 401
    data = request.get_json()
    teks = data["teks"]
    kategori = data["kategori"]
    simpan_keluhan(
        session["nim"],
        teks,
        kategori
    )
    return jsonify({
        "success": True,
        "message": "Keluhan berhasil dikirim."
    })

if __name__ == "__main__":
    app.run(debug=True)