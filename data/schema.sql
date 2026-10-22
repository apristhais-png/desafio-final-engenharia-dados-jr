-- Mini Loja Segplan: criação das tabelas
-- Apaga as tabelas antigas (filhas primeiro) para poder recriar o banco do zero.
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

-- Quem compra na loja
CREATE TABLE clientes (
    id            INTEGER PRIMARY KEY,
    nome          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    cidade        TEXT    NOT NULL,
    data_cadastro TEXT    NOT NULL  -- formato AAAA-MM-DD
);

-- O que a loja vende
CREATE TABLE produtos (
    id        INTEGER PRIMARY KEY,
    nome      TEXT    NOT NULL,
    categoria TEXT    NOT NULL,
    preco     REAL    NOT NULL CHECK (preco > 0),
    estoque   INTEGER NOT NULL CHECK (estoque >= 0)
);

-- Cada compra feita por um cliente
CREATE TABLE pedidos (
    id          INTEGER PRIMARY KEY,
    cliente_id  INTEGER NOT NULL,
    data_pedido TEXT    NOT NULL,  -- formato AAAA-MM-DD
    status      TEXT    NOT NULL CHECK (status IN ('pendente', 'pago', 'enviado', 'cancelado')),
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

-- Os produtos dentro de cada pedido (liga pedidos a produtos)
CREATE TABLE itens_pedido (
    id             INTEGER PRIMARY KEY,
    pedido_id      INTEGER NOT NULL,
    produto_id     INTEGER NOT NULL,
    quantidade     INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL    NOT NULL CHECK (preco_unitario > 0),  -- preço no dia da compra
    FOREIGN KEY (pedido_id)  REFERENCES pedidos (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);
