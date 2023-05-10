DROP procedure IF EXISTS `RevenueAddress_GetList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `RevenueAddress_GetList`(
    p_userId INT(10),
    p_currencyId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该币
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT id FROM Currency WHERE id = p_currencyId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;
    SELECT id, address, notes FROM RevenueAddress WHERE userId = p_userId AND currencyId = p_currencyId;
END ;;
DELIMITER ;