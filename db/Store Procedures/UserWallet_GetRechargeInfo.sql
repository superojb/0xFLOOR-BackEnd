DROP procedure IF EXISTS `UserWallet_GetRechargeInfo`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_GetRechargeInfo`(
    p_userId INT(10)
)
/**
  code = 0 = OK
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT
        C.currencyId,
        C.imgUrl AS logo,
        C.nickname,
        C.name,
        UW.address
    FROM `0xFLOOR`.Currency AS C
    INNER JOIN `0xFLOOR`.UserWallet AS UW ON C.currencyId = UW.currencyId AND UW.userId = p_userId
    INNER JOIN CurrencyNetwork AS CN ON C.currencyId = CN.currencyId AND CN.status = 1;

    SELECT
        currencyNetworkId,
        currencyId,
        name
    FROM CurrencyNetwork WHERE status = 1;

END ;;
DELIMITER ;