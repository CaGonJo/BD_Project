--1)

SELECT
    p.product_ean, p.descr
FROM
    product AS p
INNER JOIN
    replenishment_event AS r
    ON r.product_ean=p.product_ean
INNER JOIN
    has AS h
    ON h.product_ean=p.product_ean
WHERE
    r.instant > 4
    AND r.units > 10
    AND h.categ_name='Doces'

--2)

SELECT
    p.serial_number AS IVM_Serial_Number
FROM
    planogram AS p
WHERE
    p.product_ean=234
GROUP BY
    p.serial_number

--3)

SELECT
    COUNT(h.sub_category_name) AS sub_categ_count
FROM
    has_other AS h
WHERE
    h.super_category_name='Doces'
GROUP BY
    h.super_category_name


--4)

WITH t1 AS (
    SELECT p.product_ean, p.descr, SUM(r.units) AS units_sum
	FROM product AS p
    NATURAL JOIN replenishment_event AS r
    GROUP BY p.product_ean)

SELECT
    t1.product_ean, t1.descr
FROM
    t1
WHERE
    t1.units_sum = (SELECT MAX(units_sum)
                    FROM t1)