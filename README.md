# Mini Loja Segplan

Projeto acadêmico do **Desafio Final da Trilha de Engenharia de Dados JR**.
Uma loja virtual simples, com banco **SQLite**, consultas em **SQL** e relatórios em **Python**.

> Todos os dados são **fictícios**, criados apenas para estudo.

## Estrutura de pastas

```
.
├── data/
│   ├── schema.sql     # criação das tabelas
│   └── seed.sql       # dados fictícios
├── src/
│   └── database.py    # conecta e monta o banco
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

O comando cria o arquivo `data/loja.db` com as tabelas e os dados de exemplo.
