import sqlite3

# Conecta (ou cria) o banco de dados
conexao = sqlite3.connect("banco.db")

cursor = conexao.cursor()

# ==========================
# TABELA DE ADMINISTRADORES
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
""")

# ==========================
# TABELA DE IMÓVEIS
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco TEXT NOT NULL,
    bairro TEXT NOT NULL,
    dormitorios INTEGER,
    vagas INTEGER,
    imagem TEXT
)
""")

# ==========================
# CRIA O ADMINISTRADOR PADRÃO
# ==========================
cursor.execute("""
INSERT OR IGNORE INTO administradores
(usuario, senha)
VALUES
('admin', '123456')
""")
cursor.execute("""
INSERT INTO imoveis (titulo, descricao, preco, bairro, dormitorios, vagas, imagem)
VALUES
('Apartamento Vila Carrão', 'Ótima localização', 'R$ 289.900', 'Vila Carrão', 2, 1, ''),
('Apartamento Mooca', 'Próximo ao metrô', 'R$ 399.900', 'Mooca', 3, 1, ''),
('Apartamento Tatuapé', 'Alto padrão', 'R$ 520.000', 'Tatuapé', 2, 2, '')
""")
conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso!")