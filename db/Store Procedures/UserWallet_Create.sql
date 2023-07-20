DROP procedure IF EXISTS `UserWallet_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_Create`(
    p_userId INT(10),
    p_currencyId INT(10),
    p_address VARCHAR(200),
    p_privateKey VARCHAR(200),
    p_register BOOLEAN
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 3 = 没有该币
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT currencyId FROM Currency WHERE currencyId = p_currencyId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    INSERT UserWallet (userId, address, privateKey, register, balance, freeze, thaw, cashOut, currencyId)
    VALUE  (p_userId, p_address, p_privateKey, p_register, 0, 0, 0, 0, p_currencyId);

    COMMIT;
    SELECT 0 AS code;
END ;;
DELIMITER ;