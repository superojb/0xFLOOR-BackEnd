DROP procedure IF EXISTS `User_GetWallet`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `User_GetWallet`(
    p_UserId INT(10),
    p_currencyId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有该用户
  code = 2 = 没有该货币
 */
label:BEGIN

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_UserId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT currencyId FROM Currency WHERE currencyId = p_currencyId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT
        C.name,
        UW.address,
        UW.cashOut,
        UW.freeze,
        UW.balance,
        UW.thaw
    FROM UserWallet AS UW
    INNER JOIN `0xFLOOR`.Currency AS C ON UW.currencyId = C.currencyId
    WHERE UW.userId = p_UserId AND UW.currencyId = p_currencyId;

END ;;
DELIMITER ;