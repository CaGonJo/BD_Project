4)
SELECT Product.ean, Product.descr
FROM Product as p natural join 
	((SELECT ean, max_units
	FROM (SELECT ean, sum(units)
		FROM replenishment_event
		GROUP BY ean)
	WHERE max_units = max(units)))


SELECT Product.ean, Product.descr
FROM Product as p inner join 
	((SELECT ean, max_units
	FROM (SELECT ean, sum(units)
		FROM replenishment_event
		GROUP BY ean)
	WHERE max_units = max(units)) as aux_table)
ON p.ean == aux_table.ean

3)

SELECT count(sub_category_name)		
FROM has_other
WHERE super_category_name = 'Sopas Take-Away'

2)				(shelve é uma entidade fraca, portanto já tem lá o serial number)

SELECT serial_number
FROM planogram as p
WHERE p.ean = '9002490100070'

1)
SELECT ean, descr
FROM has natural join
	(SELECT ean, descr
	FROM Product natural join	
		(SELECT ean, sum_of_units
		FROM replenishment_event
		WHERE instant > 2021/12/31 and sum_of_units = sum(units) and sum_of_units > 10
		GROUP BY ean)
	)
WHERE name == 'Barras Energéticas'
	