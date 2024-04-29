-- Script to drop non-essential databases with a stored procedure
DELIMITER $$

DROP PROCEDURE IF EXISTS DropNonEssentialDatabases$$
CREATE PROCEDURE DropNonEssentialDatabases()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE dbName VARCHAR(64);
    DECLARE dbCursor CURSOR FOR 
        SELECT schema_name FROM information_schema.schemata 
        WHERE schema_name NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN dbCursor;

    read_loop: LOOP
        FETCH dbCursor INTO dbName;
        IF done THEN
            LEAVE read_loop;
        END IF;
        SET @s = CONCAT('DROP DATABASE ', dbName);
        PREPARE stmt FROM @s;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;

    CLOSE dbCursor;
END$$

DELIMITER ;

-- Execute the procedure
CALL DropNonEssentialDatabases();

-- Optionally, drop the procedure if it's no longer needed
DROP PROCEDURE IF EXISTS DropNonEssentialDatabases;
