-- DataShop: dados fictícios (nomes e e-mails inventados)

INSERT INTO clientes (id, nome, email, cidade, data_cadastro) VALUES
    (1, 'Ana Ribeiro',     'ana.ribeiro@exemplo.com',     'Goiânia',           '2026-01-10'),
    (2, 'Bruno Carvalho',  'bruno.carvalho@exemplo.com',  'Anápolis',          '2026-01-22'),
    (3, 'Carla Mendes',    'carla.mendes@exemplo.com',    'Aparecida de Goiânia', '2026-02-05'),
    (4, 'Diego Lima',      'diego.lima@exemplo.com',      'Goiânia',           '2026-02-18'),
    (5, 'Elisa Fonseca',   'elisa.fonseca@exemplo.com',   'Rio Verde',         '2026-03-03'),
    (6, 'Fábio Teixeira',  'fabio.teixeira@exemplo.com',  'Catalão',           '2026-03-15');

INSERT INTO produtos (id, nome, categoria, preco, estoque) VALUES
    (1, 'Caderno universitário 200 folhas', 'Papelaria',   24.90, 120),
    (2, 'Caneta esferográfica azul (cx 10)', 'Papelaria',  18.50, 200),
    (3, 'Mouse sem fio',                     'Informática', 59.90,  45),
    (4, 'Teclado USB',                       'Informática', 89.00,  30),
    (5, 'Garrafa térmica 500 ml',            'Utilidades',  49.90,  60),
    (6, 'Mochila para notebook',             'Acessórios', 149.00,  25),
    (7, 'Fone de ouvido com microfone',      'Informática', 119.90, 35);

INSERT INTO pedidos (id, cliente_id, data_pedido, status) VALUES
    (1, 1, '2026-03-20', 'enviado'),
    (2, 2, '2026-03-25', 'pago'),
    (3, 1, '2026-04-02', 'pago'),
    (4, 3, '2026-04-08', 'pendente'),
    (5, 4, '2026-04-15', 'enviado'),
    (6, 5, '2026-04-21', 'cancelado'),
    (7, 2, '2026-05-02', 'enviado'),
    (8, 6, '2026-05-10', 'pago');

INSERT INTO itens_pedido (id, pedido_id, produto_id, quantidade, preco_unitario) VALUES
    (1,  1, 1, 3,  24.90),
    (2,  1, 2, 1,  18.50),
    (3,  2, 3, 1,  59.90),
    (4,  2, 4, 1,  89.00),
    (5,  3, 5, 2,  49.90),
    (6,  4, 6, 1, 149.00),
    (7,  5, 7, 1, 119.90),
    (8,  5, 3, 1,  59.90),
    (9,  6, 1, 5,  24.90),
    (10, 7, 2, 4,  18.50),
    (11, 7, 6, 1, 149.00),
    (12, 8, 4, 2,  89.00);
