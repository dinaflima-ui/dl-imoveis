from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chave-secreta-cury"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db_connection():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# HOME
# =========================
@app.route("/")
def index():
    conn = get_db_connection()
    imoveis = conn.execute("SELECT * FROM imoveis").fetchall()
    conn.close()
    return render_template("index.html", imoveis=imoveis)


# =========================
# PÁGINA DO IMÓVEL
# =========================
@app.route("/imovel/<int:id>")
def imovel(id):

    conn = get_db_connection()
    imovel = conn.execute("SELECT * FROM imoveis WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("imovel.html", imovel=imovel)


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = get_db_connection()
        admin = conn.execute(
            "SELECT * FROM administradores WHERE usuario=? AND senha=?",
            (usuario, senha)
        ).fetchone()
        conn.close()

        if admin:
            session["admin"] = usuario
            return redirect("/admin")

        return "Login inválido"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


# =========================
# ADMIN
# =========================
@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    imoveis = conn.execute("SELECT * FROM imoveis").fetchall()
    conn.close()

    return render_template("admin.html", imoveis=imoveis)


# =========================
# NOVO IMÓVEL
# =========================
@app.route("/novo_imovel", methods=["GET", "POST"])
def novo_imovel():

    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        bairro = request.form["bairro"]
        dormitorios = request.form["dormitorios"]
        vagas = request.form["vagas"]

        imagem = request.files["imagem"]
        filename = ""

        if imagem:
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO imoveis
            (titulo, descricao, preco, bairro, dormitorios, vagas, imagem)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titulo, descricao, preco, bairro, dormitorios, vagas, filename))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("novo_imovel.html")


# =========================
# EDITAR IMÓVEL
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    imovel = conn.execute("SELECT * FROM imoveis WHERE id=?", (id,)).fetchone()

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        bairro = request.form["bairro"]
        dormitorios = request.form["dormitorios"]
        vagas = request.form["vagas"]

        conn.execute("""
            UPDATE imoveis SET
            titulo=?, descricao=?, preco=?, bairro=?, dormitorios=?, vagas=?
            WHERE id=?
        """, (titulo, descricao, preco, bairro, dormitorios, vagas, id))

        conn.commit()
        conn.close()

        return redirect("/admin")

    conn.close()
    return render_template("editar.html", imovel=imovel)


# =========================
# EXCLUIR IMÓVEL
# =========================
@app.route("/deletar/<int:id>")
def deletar(id):

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    conn.execute("DELETE FROM imoveis WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
if __name__ == "__main__":
    app.run()