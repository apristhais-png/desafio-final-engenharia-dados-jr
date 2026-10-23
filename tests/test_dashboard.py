"""Confere se os cálculos do dashboard (pandas) batem com o SQL do projeto.

Como rodar:  python tests/test_dashboard.py   (o banco precisa existir)
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "dashboard"))

import dados  # noqa: E402  (dados.py também deixa src/ disponível)
import queries  # noqa: E402

ITENS = dados.carregar_itens()


def sql(comando):
    return queries.executar_consulta(comando)[0][0]


def test_faturamento_exclui_cancelados():
    esperado = sql("SELECT ROUND(SUM(total), 2) FROM vw_total_por_pedido WHERE status <> 'cancelado'")
    assert dados.calcular_indicadores(ITENS)["faturamento"] == esperado


def test_total_de_pedidos_e_ticket_medio():
    ind = dados.calcular_indicadores(ITENS)
    assert ind["total_pedidos"] == sql("SELECT COUNT(*) FROM pedidos")
    esperado = sql("SELECT ROUND(AVG(total), 2) FROM vw_total_por_pedido WHERE status <> 'cancelado'")
    assert ind["ticket_medio"] == esperado


def test_cadastros():
    assert dados.contar_cadastros() == (sql("SELECT COUNT(*) FROM clientes"),
                                         sql("SELECT COUNT(*) FROM produtos"))


def test_faturamento_por_categoria_igual_ao_queries():
    tabela = dados.faturamento_por_categoria(ITENS)
    calculado = {cat: round(v, 2) for cat, v in zip(tabela["categoria"], tabela["valor"])}
    assert calculado == {cat: total for cat, _, total in queries.faturamento_por_categoria()}


def test_ranking_clientes_igual_ao_queries():
    tabela = dados.ranking_clientes(ITENS)
    calculado = {c: (p, round(t, 2)) for c, t, p in tabela[["cliente", "total", "pedidos"]].itertuples(index=False)}
    assert calculado == {c: (p, t) for c, p, t in queries.clientes_que_mais_gastam()}


def test_pedidos_por_status():
    tabela = dados.pedidos_por_status(ITENS)
    esperado = dict(queries.executar_consulta("SELECT status, COUNT(*) FROM pedidos GROUP BY status"))
    assert dict(zip(tabela["status"], tabela["pedidos"])) == esperado


def test_vendas_por_mes():
    tabela = dados.vendas_por_mes(ITENS)
    esperado = queries.executar_consulta(
        "SELECT substr(data_pedido, 1, 7), ROUND(SUM(total), 2) FROM vw_total_por_pedido "
        "WHERE status <> 'cancelado' GROUP BY 1 ORDER BY 1")
    calculado = [(m.strftime("%Y-%m"), round(v, 2)) for m, v in zip(tabela["mes"], tabela["faturamento"])]
    assert calculado == esperado


def test_produtos_mais_vendidos():
    tabela = dados.produtos_mais_vendidos(ITENS)
    esperado = dict(queries.executar_consulta(
        "SELECT pr.nome, SUM(i.quantidade) FROM itens_pedido i "
        "JOIN produtos pr ON pr.id = i.produto_id JOIN pedidos p ON p.id = i.pedido_id "
        "WHERE p.status <> 'cancelado' GROUP BY pr.nome"))
    assert dict(zip(tabela["produto"], tabela["quantidade"])) == esperado


def test_filtros():
    so_info = dados.filtrar(ITENS, ["Informática"], ITENS["status"].unique(), "2026-01-01", "2026-12-31")
    assert set(so_info["categoria"]) == {"Informática"}
    esperado = [t for c, _, t in queries.faturamento_por_categoria() if c == "Informática"][0]
    assert dados.calcular_indicadores(so_info)["faturamento"] == esperado

    so_cancelados = dados.filtrar(ITENS, ITENS["categoria"].unique(), ["cancelado"], "2026-01-01", "2026-12-31")
    assert dados.calcular_indicadores(so_cancelados)["faturamento"] == 0

    abril = dados.filtrar(ITENS, ITENS["categoria"].unique(), ITENS["status"].unique(), "2026-04-01", "2026-04-30")
    assert set(abril["data_pedido"].dt.month) == {4}


if __name__ == "__main__":
    testes = [f for nome, f in sorted(globals().items()) if nome.startswith("test_")]
    for teste in testes:
        teste()
        print(f"OK  {teste.__name__}")
    print(f"\n{len(testes)} testes passaram.")
