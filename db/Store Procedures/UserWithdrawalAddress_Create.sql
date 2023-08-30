DROP procedure IF EXISTS `UserWithdrawalAddress_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWithdrawalAddress_Create`(
    p_userId INT(10),
    p_currencyId INT(10),
    p_currencyNetworkId INT(10),
    p_notes VARCHAR(200),
    p_address VARCHAR(200)
)
/**
  code = 0 = OK
  code = 1 = User 不存在
  code = 2 = 该货币 不存在
  code = 3 = 该网络 不存在
  code = 4 = 该地址已存在

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

    IF NOT EXISTS(SELECT currencyId FROM CurrencyNetwork WHERE currencyNetworkId = p_currencyNetworkId AND currencyId = p_currencyId) THEN
        SELECT 3 AS code;
        LEAVE label;
    END IF ;

    IF EXISTS(SELECT userId FROM WithdrawalAddress WHERE userId = p_userId AND address = p_address) THEN
        SELECT 4 AS code;
        LEAVE label;
    END IF ;

    INSERT WithdrawalAddress (userId, address, notes, currencyId, currencyNetworkId)
    VALUE (p_userId, p_address, p_notes, p_currencyId, p_currencyNetworkId);
    COMMIT;

    SELECT 0 AS code;

END ;;
DELIMITER ;