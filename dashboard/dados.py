"""Camada de dados do dashboard: lê o SQLite e calcula os indicadores com pandas."""

import sys
from pathlib import Path

import pandas as pd

# Permite importar os módulos de src/ (reaproveitamos a conexão do projeto)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from database import CAMINHO_BANCO, conectar  # noqa: E402

STATUS_CANCELADO = "cancelado"

# Uma linha por item vendido, já com cliente, produto e pedido (JOIN das 4 tabelas)
SQL_ITENS = """
    SELECT p.id          AS pedido_id,
           p.data_pedido,
           p.status,
           c.nome        AS cliente,
           pr.nome       AS produto,
           pr.categoria,
           i.quantidade,
           i.preco_unitario,
           i.quantidade * i.preco_unitario AS valor
    FROM itens_pedido i
    JOIN pedidos  p  ON p.id  = i.pedido_id
    JOIN clientes c  ON c.id  = p.cliente_id
    JOIN produtos pr ON pr.id = i.produto_id
"""


def banco_existe():
    """O banco existe se o arquivo loja.db já foi criado pelo database.py."""
    return CAMINHO_BANCO.exists()


def carregar_itens():
    """Lê os itens vendidos do SQLite e devolve um DataFrame (tabela do pandas)."""
    with conectar() as conexao:
        itens = pd.read_sql_query(SQL_ITENS, conexao)
    itens["data_pedido"] = pd.to_datetime(itens["data_pedido"])
    itens["mes"] = itens["data_pedido"].dt.to_period("M").dt.to_timestamp()
    return itens


def contar_cadastros():
    """Quantidade de clientes e produtos cadastrados (não depende dos filtros)."""
    with conectar() as conexao:
        clientes = conexao.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        produtos = conexao.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    return clientes, produtos


def filtrar(itens, categorias, status, data_inicio, data_fim):
    """Aplica os filtros escolhidos na barra lateral."""
    filtro = (
        itens["categoria"].isin(categorias)
        & itens["status"].isin(status)
        & itens["data_pedido"].between(pd.Timestamp(data_inicio), pd.Timestamp(data_fim))
    )
    return itens[filtro]


def vendas_validas(itens):
    """Remove os pedidos cancelados: eles não entram no faturamento."""
    return itens[itens["status"] != STATUS_CANCELADO]


def calcular_indicadores(itens):
    """Faturamento, total de pedidos e ticket médio (pedidos válidos)."""
    validos = vendas_validas(itens)
    faturamento = round(validos["valor"].sum(), 2)
    pedidos_validos = validos["pedido_id"].nunique()
    return {
        "faturamento": faturamento,
        "total_pedidos": itens["pedido_id"].nunique(),
        "pedidos_cancelados": itens.loc[itens["status"] == STATUS_CANCELADO, "pedido_id"].nunique(),
        "ticket_medio": round(faturamento / pedidos_validos, 2) if pedidos_validos else 0.0,
    }


def faturamento_por_categoria(itens):
    return (
        vendas_validas(itens)
        .groupby("categoria", as_index=False)["valor"].sum()
        .sort_values("valor")
    )


def pedidos_por_status(itens):
    return (
        itens.groupby("status", as_index=False)["pedido_id"].nunique()
        .rename(columns={"pedido_id": "pedidos"})
        .sort_values("pedidos", ascending=False)
    )


def vendas_por_mes(itens):
    return (
        vendas_validas(itens)
        .groupby("mes", as_index=False)
        .agg(faturamento=("valor", "sum"), pedidos=("pedido_id", "nunique"))
        .sort_values("mes")
    )


def ranking_clientes(itens):
    return (
        vendas_validas(itens)
        .groupby("cliente", as_index=False)
        .agg(total=("valor", "sum"), pedidos=("pedido_id", "nunique"))
        .sort_values("total")
    )


def produtos_mais_vendidos(itens):
    return (
        vendas_validas(itens)
        .groupby(["produto", "categoria"], as_index=False)
        .agg(quantidade=("quantidade", "sum"), valor=("valor", "sum"))
        .sort_values(["quantidade", "valor"])
    )
