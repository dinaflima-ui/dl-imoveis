from flask import Flask, render_template

app = Flask(__name__)

# Página inicial
@app.route("/")
def index():
    imoveis = []
    return render_template("index.html", imoveis=imoveis)

# Área admin
@app.route("/admin")
def admin():
    imoveis = []
    return render_template("admin.html", imoveis=imoveis)

# Login
@app.route("/login")
def login():
    return render_template("login.html")

# Página de novo imóvel
@app.route("/novo-imovel")
def novo_imovel():
    return render_template("novo_imovel.html")


# IMPORTANTE: isso precisa estar indentado corretamente
if __name__ == "__main__":
    app.run()