"""Conexão com o banco SQLite e criação das tabelas da Mini Loja Segplan."""

import sqlite3
from pathlib import Path

# Caminhos calculados a partir deste arquivo, para funcionar de qualquer pasta
PASTA_DATA = Path(__file__).resolve().parent.parent / "data"
CAMINHO_BANCO = PASTA_DATA / "loja.db"


def conectar():
    """Abre a conexão com o banco e liga a checagem de chaves estrangeiras."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")  # no SQLite isso vem desligado
    return conexao


def executar_arquivo_sql(conexao, nome_arquivo):
    """Lê um arquivo .sql da pasta data/ e executa todos os comandos dele."""
    sql = (PASTA_DATA / nome_arquivo).read_text(encoding="utf-8")
    conexao.executescript(sql)


def criar_banco():
    """Recria o banco do zero: tabelas, dados fictícios e views."""
    try:
        with conectar() as conexao:
            executar_arquivo_sql(conexao, "schema.sql")
            executar_arquivo_sql(conexao, "seed.sql")
            executar_arquivo_sql(conexao, "views.sql")
        print(f"Banco criado com sucesso em: {CAMINHO_BANCO}")
    except (sqlite3.Error, OSError) as erro:
        print(f"Erro ao criar o banco: {erro}")


if __name__ == "__main__":
    criar_banco()
