# Mini Loja Segplan

Projeto acadêmico do **Desafio Final da Trilha de Engenharia de Dados JR**.
Uma loja virtual simples, com banco **SQLite**, consultas em **SQL** e relatórios em **Python**.

> Todos os dados são **fictícios**, criados apenas para estudo.

## Estrutura de pastas

```
.
├── data/
│   ├── schema.sql     # criação das tabelas
│   ├── seed.sql       # dados fictícios
│   └── views.sql      # view vw_total_por_pedido
├── src/
│   ├── database.py    # conecta e monta o banco
│   ├── queries.py     # consultas SQL (uma função por consulta)
│   └── main.py        # menu interativo no terminal
├── requirements.txt
└── README.md
```

## Modelo de dados

```
clientes 1 ──< N pedidos 1 ──< N itens_pedido >── 1 produtos
```

| Tabela         | O que guarda                          | Chave estrangeira                     |
|----------------|---------------------------------------|---------------------------------------|
| `clientes`     | quem compra                           | —                                     |
| `produtos`     | o que a loja vende                    | —                                     |
| `pedidos`      | cada compra feita por um cliente      | `cliente_id` → `clientes.id`          |
| `itens_pedido` | os produtos dentro de cada pedido     | `pedido_id` → `pedidos.id`, `produto_id` → `produtos.id` |

## Como rodar

Requisito: Python 3.10 ou superior (não precisa instalar nada além dele).

```bash
python src/database.py
```

O comando cria o arquivo `data/loja.db` com as tabelas, os dados de exemplo e a view.

Depois, abra o menu interativo:

```bash
python src/main.py
```

```
===== Mini Loja Segplan =====
1. Listar pedidos com clientes
2. Consultar produtos por categoria
3. Ver faturamento por categoria
4. Ver clientes que mais gastam
5. Ver ticket médio por status
6. Sair
Escolha uma opção:
```

Digite o número da opção e tecle Enter. O menu fica aberto até você escolher `6`.
Entradas inválidas (letras ou números fora da lista) mostram um aviso e o menu volta.

Para ver o resultado bruto das consultas, sem menu:

```bash
python src/queries.py
```

## Consultas

| Função | O que responde | Recursos SQL |
|---|---|---|
| `listar_categorias` | Quais categorias existem? | `DISTINCT` |
| `listar_pedidos_com_clientes` | Quem fez cada pedido? | `JOIN` |
| `produtos_por_categoria` | Quais produtos são de uma categoria? | `WHERE` |
| `faturamento_por_categoria` | Quanto cada categoria vendeu? | `JOIN`, `WHERE`, `GROUP BY`, `SUM` |
| `clientes_que_mais_gastam` | Quem mais gastou? | `VIEW`, `GROUP BY`, `COUNT`, `SUM` |
| `ticket_medio_por_status` | Qual o valor médio por status? | `VIEW`, `GROUP BY`, `AVG` |
