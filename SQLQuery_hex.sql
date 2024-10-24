/*
-- Consulta para obter detalhes dos pedidos de venda, incluindo data, total devido, estado e produto.
-- Autoria: [Rodrigo Alves]
-- Data: [23/10/2024]
-- Descri��o: Esta consulta seleciona informa��es de pedidos de venda, formatando o total devido
-- no formato monet�rio brasileiro e unindo tabelas relevantes para trazer dados de pedidos, produtos e endere�os.
-- Tabelas usadas:
-- - Sales.SalesOrderHeader: Informa��es sobre os pedidos de venda.
-- - Sales.SalesOrderDetail: Detalhes dos produtos em cada pedido.
-- - Person.Address: Endere�os de entrega.
-- - Production.Product: Informa��es sobre produtos.
*/

SELECT
    --soh.SalesOrderID,
    soh.OrderDate AS DATA,
    FORMAT(soh.TotalDue, 'C', 'pt-BR') AS TOTAL_DEVIDO,
    --CONVERT(INT, soh.TotalDue) AS TOTAL_DEVIDO,
    --sod.ProductID,
    --soh.ShipToAddressID,
    addr.StateProvinceID AS ESTADO,
    p.Name AS PRODUTO
FROM 
    [Sales].[SalesOrderHeader] soh
JOIN [Sales].[SalesOrderDetail] sod
    ON soh.SalesOrderID = sod.SalesOrderID
JOIN [Person].[Address] addr
    ON soh.ShipToAddressID = addr.AddressID
JOIN [Production].[Product] p
    ON sod.ProductID = p.ProductID;
