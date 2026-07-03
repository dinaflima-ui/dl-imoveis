import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect
import urllib.parse

app = Flask(__name__)

# 📦 BANCO DE DADOS
def init_db():
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        imovel TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# 🏠 Página inicial
@app.route("/")
def index():
    imoveis = []
    return render_template("index.html", imoveis=imoveis)

# 🔐 Admin
@app.route("/admin")
def admin():
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()

    c.execute("SELECT * FROM leads ORDER BY id DESC")
    leads = c.fetchall()

    conn.close()

    return render_template("admin.html", leads=leads)

# 🔑 Login
@app.route("/login")
def login():
    return render_template("login.html")

# ➕ Novo imóvel
@app.route("/novo-imovel")
def novo_imovel():
    return render_template("novo_imovel.html")

# 📅 CRM + WhatsApp
@app.route("/visita", methods=["GET", "POST"])
def visita():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        imovel = request.form["imovel"]

        # salvar no banco
        conn = sqlite3.connect("leads.db")
        c = conn.cursor()

        c.execute("""
            INSERT INTO leads (nome, telefone, imovel, data)
            VALUES (?, ?, ?, ?)
        """, (nome, telefone, imovel, datetime.now()))

        conn.commit()
        conn.close()

        # mensagem WhatsApp
        mensagem = f"""
Olá! Tenho interesse em agendar uma visita.

Nome: {nome}
Telefone: {telefone}
Imóvel: {imovel}
"""

        mensagem_codificada = urllib.parse.quote(mensagem)

        numero_whatsapp = "5511988798286"

        link = f"https://wa.me/{numero_whatsapp}?text={mensagem_codificada}"

        return redirect(link)

    return render_template("visita.html")


if __name__ == "__main__":
    app.run(debug=True)