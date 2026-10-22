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
│   └── queries.py     # consultas SQL (uma função por consulta)
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

Para ver o resultado das consultas:

```bash
python src/queries.py
```

## Consultas

| Função | O que responde | Recursos SQL |
|---|---|---|
| `listar_pedidos_com_clientes` | Quem fez cada pedido? | `JOIN` |
| `produtos_por_categoria` | Quais produtos são de uma categoria? | `WHERE` |
| `faturamento_por_categoria` | Quanto cada categoria vendeu? | `JOIN`, `WHERE`, `GROUP BY`, `SUM` |
| `clientes_que_mais_gastam` | Quem mais gastou? | `VIEW`, `GROUP BY`, `COUNT`, `SUM` |
| `ticket_medio_por_status` | Qual o valor médio por status? | `VIEW`, `GROUP BY`, `AVG` |
