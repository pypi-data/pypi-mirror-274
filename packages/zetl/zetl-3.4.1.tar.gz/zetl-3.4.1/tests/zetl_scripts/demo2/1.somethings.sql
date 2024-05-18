/*
  -- Dave Skura, 2022

DB_TYPE		= MySQL
DB_USERNAME	= root
DB_USERPWD  = 4165605869
DB_HOST		= localhost
DB_PORT		= 3306
DB_NAME		= atlas
DB_SCHEMA	= not_used_for_mysql

*/

DROP TABLE IF EXISTS thistable;

CREATE TABLE thistable AS
SELECT CURRENT_DATE as rightnow
WHERE 1 = 1;

SELECT *
FROM thistable;