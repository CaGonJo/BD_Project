--1)

SELECT
    p.ean, p.descr
FROM
    Product AS p
INNER JOIN
    Replenishment_event AS r
    ON r.ean=p.ean
INNER JOIN
    has AS h
    ON h.ean=p.ean
WHERE
    r.instant > 2021/12/31 23:59
    AND r.units > 10
    AND h.categ_name='Barras Energéticas'

--2)

SELECT
    p.serial_number
FROM
    planogram AS p
WHERE
    p._ean=9002490100070
GROUP BY
    p.serial_number

--3)

SELECT
    COUNT(h.sub_category_name) AS sub_categ_count
FROM
    has_other AS h
WHERE
    h.super_category_name='Sopas Take-Away'
GROUP BY
    h.super_category_name


--4)

WITH t1 AS (
    SELECT p.ean, p.descr, SUM(r.units) AS units_sum
	FROM Product AS p
    NATURAL JOIN Replenishment_event AS r
    GROUP BY p.ean)

SELECT
    t1.ean, t1.descr
FROM
    t1
WHERE
    t1.units_sum = (SELECT MAX(units_sum)
                    FROM t1)