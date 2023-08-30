DROP procedure IF EXISTS `UserWallet_ConfirmedTransaction`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_ConfirmedTransaction`(
    p_UserWalletLogId INT(10)
)
/**
  code = 0 = OK
 */
label:BEGIN
    DECLARE v_type INT;
    DECLARE v_userId INT;
    DECLARE v_currencyId INT;
    DECLARE v_changeAmount double;

    SELECT
        type,
        userId,
        currencyId,
        changeAmount
    INTO
        v_type,
        v_userId,
        v_currencyId,
        v_changeAmount
    FROM UserWalletLog WHERE UserWalletLogId = p_UserWalletLogId;

    UPDATE UserWalletLog SET status = 2, updateTime = NOW() WHERE UserWalletLogId = p_UserWalletLogId;

    -- 充值
    IF v_type = 1 THEN
        UPDATE UserWallet SET balance = balance + v_changeAmount WHERE userId = v_userId AND currencyId = v_currencyId;
    END IF ;

    COMMIT;
    SELECT 0 AS code;

END ;;
DELIMITER ;