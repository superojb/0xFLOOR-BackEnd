DROP procedure IF EXISTS `RevenueAddress_Delete`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `RevenueAddress_Delete`(
    p_id INT(10),
    p_userId INT(10)
)
/**
  code = 0 = OK
  code = 5 = 不能删除不是自己的收益地址
 */
label:BEGIN
    IF not EXISTS(SELECT id FROM RevenueAddress WHERE id = p_id AND userId = p_userId) THEN
        SELECT 5 AS code;
        LEAVE label;
    END IF ;
    SELECT 0 AS code;
    DELETE FROM RevenueAddress WHERE id = p_id;
END ;;
DELIMITER ;