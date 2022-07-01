------- DATABASES ---------
CREATE DATABASE IF NOT EXISTS DB_TEST
DEFAULT CHARACTER SET UTF8;

------- PROCEDURES ---------
USE DB_TEST;

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS PR_CLEAN_DB()
BEGIN
    CALL PR_QUERY_EXECUTOR('SET FOREIGN_KEY_CHECKS = 0;');
    CALL PR_QUERY_EXECUTOR('TRUNCATE TABLE itens_notas_fiscais;');
    CALL PR_QUERY_EXECUTOR('TRUNCATE TABLE notas_fiscais;');
    CALL PR_QUERY_EXECUTOR('SET FOREIGN_KEY_CHECKS = 1;');  
END $$
DELIMITER ;

DELIMITER &&
CREATE PROCEDURE IF NOT EXISTS PR_QUERY_EXECUTOR(QUERY LONGTEXT)
BEGIN
    PREPARE SMT FROM QUERY;
    EXECUTE SMT;
    DEALLOCATE PREPARE SMT;
END &&
DELIMITER ;

------- CREATE TABLES ---------
CREATE TABLE IF NOT EXISTS round_statistics (
    id int NOT NULL, 
    quantity int, 
    operator_total_time float, 
    function_total_time float, 
    operator varchar(20) NOT NULL, 
    date_info date NOT NULL DEFAULT CURDATE(),
    primary key(id, operator, date_info));