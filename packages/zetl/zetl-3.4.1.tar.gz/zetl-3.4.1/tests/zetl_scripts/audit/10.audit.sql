/*
  -- Dave Skura, 2023
DB_TYPE		= MySQL
DB_USERNAME	= dbadmin
DB_USERPWD  = Na$d0m!23
DB_HOST		= 10.100.12.80
DB_PORT		= 3355
DB_NAME		= appraisal

*/

SELECT filename,sheet,action,builder_code
FROM elt.rbc_builder_code_audit
ORDER BY dtm desc
limit 50;


SELECT version();