DROP procedure IF EXISTS `UserWallet_balanceChange`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_balanceChange`(
    p_userId INT(10),
    p_currencyId INT(10),
    p_type INT(10),
    p_status INT(10),
    p_changeAmount DOUBLE,
    p_hax VARCHAR(200),
    p_transactionTime BIGINT,
    p_associateId VARCHAR(200)

)
/**
  code = 0 = OK
  code = 4 = 已有该交易
 */
label:BEGIN
    DECLARE v_balance DOUBLE;
    DECLARE v_changeAmount DOUBLE;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF EXISTS(SELECT userId FROM UserWalletLog WHERE userId = p_userId AND hax = p_hax) THEN
        SELECT 4 AS code;
        LEAVE label;
    END IF ;

    SELECT
        balance + thaw + cashOut + freeze
    INTO
        v_balance
    FROM UserWallet WHERE userId = p_userId AND currencyId = p_currencyId;
    SET v_changeAmount = IF(p_type = 1, p_changeAmount, -p_changeAmount);

    INSERT UserWalletLog (type, changeAmount, hax, status, balance, createTime, currencyId, userId, transactionTime, updateTime, associateId)
    VALUE (p_type, v_changeAmount, p_hax, p_status,
           IF(p_type = 1, v_balance + v_changeAmount, -p_changeAmount),
           NOW(), p_currencyId, p_userId, p_transactionTime, NOW(), p_associateId);

    -- 充值并且已经确认， 直接更改余额
    IF p_type = 1 AND p_status = 2 THEN
        UPDATE UserWallet
        SET balance = balance + p_changeAmount
        WHERE userId = p_userId AND currencyId = p_currencyId;

    END IF;
    COMMIT;

    SELECT 0 AS code;

END ;;
DELIMITER ;