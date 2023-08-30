DROP procedure IF EXISTS `UserWallet_GetUnConfirmedList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_GetUnConfirmedList`()
/**
  code = 0 = OK
 */
label:BEGIN
    SELECT
        UWL.UserWalletLogId,
        UWL.userId,
        UWL.changeAmount,
        UWL.type,
        UWL.hax AS TransactionId,
        C.name AS CurrencyName
    FROM UserWalletLog AS UWL
    INNER JOIN `0xFLOOR`.Currency AS C ON UWL.currencyId = C.currencyId
    WHERE UWL.status = 1;

END ;;
DELIMITER ;