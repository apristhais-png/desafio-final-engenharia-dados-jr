"""Consultas SQL da Mini Loja Segplan. Cada função devolve uma lista de linhas."""

from database import conectar


def executar_consulta(sql, parametros=()):
    """Executa um SELECT e devolve todas as linhas encontradas."""
    with conectar() as conexao:
        return conexao.execute(sql, parametros).fetchall()


def listar_pedidos_com_clientes():
    """JOIN: mostra cada pedido com o nome do cliente que comprou."""
    sql = """
        SELECT p.id, c.nome, p.data_pedido, p.status
        FROM pedidos p
        JOIN clientes c ON c.id = p.cliente_id
        ORDER BY p.id
    """
    return executar_consulta(sql)


def produtos_por_categoria(categoria):
    """WHERE: lista os produtos de uma categoria escolhida."""
    # O "?" evita SQL injection: o valor é enviado separado do comando
    sql = """
        SELECT nome, preco, estoque
        FROM produtos
        WHERE categoria = ?
        ORDER BY preco
    """
    return executar_consulta(sql, (categoria,))


def faturamento_por_categoria():
    """JOIN + WHERE + GROUP BY + SUM: quanto cada categoria vendeu (sem cancelados)."""
    sql = """
        SELECT pr.categoria,
               SUM(i.quantidade)                    AS unidades,
               ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS faturamento
        FROM itens_pedido i
        JOIN produtos pr ON pr.id = i.produto_id
        JOIN pedidos p   ON p.id = i.pedido_id
        WHERE p.status <> 'cancelado'
        GROUP BY pr.categoria
        ORDER BY faturamento DESC
    """
    return executar_consulta(sql)


def clientes_que_mais_gastam():
    """VIEW + GROUP BY + COUNT + SUM: ranking de clientes pelo total gasto."""
    sql = """
        SELECT cliente,
               COUNT(*)   AS qtd_pedidos,
               ROUND(SUM(total), 2) AS total_gasto
        FROM vw_total_por_pedido
        WHERE status <> 'cancelado'
        GROUP BY cliente
        ORDER BY total_gasto DESC
    """
    return executar_consulta(sql)


def ticket_medio_por_status():
    """VIEW + GROUP BY + AVG: valor médio dos pedidos em cada status."""
    sql = """
        SELECT status,
               COUNT(*)             AS qtd_pedidos,
               ROUND(AVG(total), 2) AS ticket_medio
        FROM vw_total_por_pedido
        GROUP BY status
        ORDER BY ticket_medio DESC
    """
    return executar_consulta(sql)


if __name__ == "__main__":
    # Teste rápido: mostra o resultado de cada consulta no terminal
    consultas = {
        "Pedidos com clientes": listar_pedidos_com_clientes(),
        "Produtos da categoria Informática": produtos_por_categoria("Informática"),
        "Faturamento por categoria": faturamento_por_categoria(),
        "Clientes que mais gastam": clientes_que_mais_gastam(),
        "Ticket médio por status": ticket_medio_por_status(),
    }
    for titulo, linhas in consultas.items():
        print(f"\n== {titulo} ==")
        for linha in linhas:
            print(linha)
