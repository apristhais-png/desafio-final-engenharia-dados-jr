"""Menu interativo no terminal da Mini Loja Segplan."""

import sqlite3

import queries


def formatar_moeda(valor):
    """Transforma 1234.5 em 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}"  # 1,234.50
    return "R$ " + texto.replace(",", "_").replace(".", ",").replace("_", ".")


def imprimir_tabela(titulo, colunas, linhas):
    """Mostra uma lista de linhas como tabela, com colunas alinhadas."""
    print(f"\n=== {titulo} ===")
    if not linhas:
        print("Nenhum resultado encontrado.")
        return
    # Largura de cada coluna = maior texto entre o título e os valores dela
    larguras = [
        max(len(str(item)) for item in [coluna] + [linha[i] for linha in linhas])
        for i, coluna in enumerate(colunas)
    ]
    print("  ".join(c.ljust(l) for c, l in zip(colunas, larguras)))
    print("  ".join("-" * l for l in larguras))
    for linha in linhas:
        print("  ".join(str(v).ljust(l) for v, l in zip(linha, larguras)))


def relatorio_pedidos():
    linhas = queries.listar_pedidos_com_clientes()
    imprimir_tabela("Pedidos com clientes", ["Pedido", "Cliente", "Data", "Status"], linhas)


def relatorio_produtos_por_categoria():
    categorias = queries.listar_categorias()
    print("\nCategorias disponíveis: " + ", ".join(categorias))
    escolha = input("Digite a categoria: ").strip()

    # Aceita a categoria sem diferenciar maiúsculas de minúsculas
    for categoria in categorias:
        if categoria.lower() == escolha.lower():
            linhas = [
                (nome, formatar_moeda(preco), estoque)
                for nome, preco, estoque in queries.produtos_por_categoria(categoria)
            ]
            imprimir_tabela(f"Produtos de {categoria}", ["Produto", "Preço", "Estoque"], linhas)
            return
    print(f"Categoria '{escolha}' não encontrada.")


def relatorio_faturamento():
    linhas = [
        (categoria, unidades, formatar_moeda(total))
        for categoria, unidades, total in queries.faturamento_por_categoria()
    ]
    imprimir_tabela("Faturamento por categoria (sem cancelados)",
                    ["Categoria", "Unidades", "Faturamento"], linhas)


def relatorio_clientes():
    linhas = [
        (cliente, qtd, formatar_moeda(total))
        for cliente, qtd, total in queries.clientes_que_mais_gastam()
    ]
    imprimir_tabela("Clientes que mais gastam (sem cancelados)",
                    ["Cliente", "Pedidos", "Total gasto"], linhas)


def relatorio_ticket_medio():
    linhas = [
        (status, qtd, formatar_moeda(media))
        for status, qtd, media in queries.ticket_medio_por_status()
    ]
    imprimir_tabela("Ticket médio por status", ["Status", "Pedidos", "Ticket médio"], linhas)


# Cada opção do menu: (texto mostrado, função que será chamada)
OPCOES = {
    1: ("Listar pedidos com clientes", relatorio_pedidos),
    2: ("Consultar produtos por categoria", relatorio_produtos_por_categoria),
    3: ("Ver faturamento por categoria", relatorio_faturamento),
    4: ("Ver clientes que mais gastam", relatorio_clientes),
    5: ("Ver ticket médio por status", relatorio_ticket_medio),
}
OPCAO_SAIR = 6


def mostrar_menu():
    print("\n===== Mini Loja Segplan =====")
    for numero, (texto, _) in OPCOES.items():
        print(f"{numero}. {texto}")
    print(f"{OPCAO_SAIR}. Sair")


def main():
    while True:
        mostrar_menu()
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida: digite apenas o número da opção.")
            continue

        if opcao == OPCAO_SAIR:
            print("Até logo!")
            break
        if opcao not in OPCOES:
            print(f"Opção inválida: escolha um número de 1 a {OPCAO_SAIR}.")
            continue

        _, funcao = OPCOES[opcao]
        try:
            funcao()
        except sqlite3.Error as erro:
            print(f"Erro ao consultar o banco: {erro}")
            print("Dica: rode 'python src/database.py' para criar o banco.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C ou fim da entrada
        print("\nPrograma encerrado.")
