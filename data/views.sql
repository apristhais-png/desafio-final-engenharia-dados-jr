-- Mini Loja Segplan: views (consultas salvas no banco)
DROP VIEW IF EXISTS vw_total_por_pedido;

-- Um resumo por pedido: cliente, data, status e valor total
CREATE VIEW vw_total_por_pedido AS
SELECT
    p.id                                  AS pedido_id,
    c.nome                                AS cliente,
    p.data_pedido,
    p.status,
    ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS total
FROM pedidos p
JOIN clientes c     ON c.id = p.cliente_id
JOIN itens_pedido i ON i.pedido_id = p.id
GROUP BY p.id;
