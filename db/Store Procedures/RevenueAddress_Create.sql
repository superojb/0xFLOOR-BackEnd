DROP procedure IF EXISTS `RevenueAddress_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `RevenueAddress_Create`(
    p_userId INT(10),
    p_currencyId INT(10),
    p_address CHAR(200),
    p_notes CHAR(200)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该币
  code = 3 = 该地址已添加
  code = 4 = 已有该备注
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

    IF EXISTS(SELECT id FROM RevenueAddress WHERE userId = p_userId AND currencyId = p_currencyId AND address = p_address) THEN
        SELECT 3 AS code;
        LEAVE label;
    END IF ;

    IF EXISTS(SELECT id FROM RevenueAddress WHERE userId = p_userId AND notes = p_notes) THEN
        SELECT 4 AS code;
        LEAVE label;
    END IF ;

    INSERT RevenueAddress (userId, currencyId, address, notes)
    VALUE (p_userId, p_currencyId, p_address, p_notes);
    COMMIT;
    SELECT 0 AS code;
END ;;
DELIMITER ;