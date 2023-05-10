DROP procedure IF EXISTS `RevenueAddress_Update`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `RevenueAddress_Update`(
    p_id INT(10),
    p_userId INT(10),
    p_notes CHAR(200)
)
/**
  code = 0 = OK
  code = 6 = 不能修改不是自己的收益地址
 */
label:BEGIN
    IF not EXISTS(SELECT id FROM RevenueAddress WHERE id = p_id AND userId = p_userId) THEN
        SELECT 5 AS code;
        LEAVE label;
    END IF ;
    SELECT 0 AS code;
    UPDATE RevenueAddress SET notes = p_notes WHERE id = p_id;
    COMMIT;
END ;;
DELIMITER ;