DROP procedure IF EXISTS `UserCashOutApply_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserCashOutApply_Create`(
    p_userId INT,
    p_amount DOUBLE,
    p_currencyNetworkId INT,
    p_address VARCHAR(200)
)

/**
  code = 0 = OK
  code = 1 = 没有该订单
  code = 2 = 没有该钱包
  code = 3 = 余额不足
  code = 4 = 该提现网络不可用
 */
label:BEGIN
    DECLARE v_balance DOUBLE;
    DECLARE v_userWalletId INT;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF;

    IF NOT EXISTS(SELECT currencyNetworkId FROM CurrencyNetwork WHERE currencyNetworkId = p_currencyNetworkId AND status = 1) THEN
        SELECT 4 AS code;
        LEAVE label;
    END IF;

    SELECT
        userWalletId,
        balance
    INTO
        v_userWalletId,
        v_balance
    FROM UserWallet WHERE userId = p_userId AND currencyId = p_currencyId;

    IF v_userWalletId IS NULL THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    IF p_amount > v_balance THEN
        SELECT 3 AS code;
        LEAVE label;
    END IF ;

    INSERT UserCashOutApply (status, address, amount, createTime, updateTime, currencyId, userId, hax)
    VALUE (1, p_address, p_amount, NOW(), NOW(), p_currencyId, p_userId, '');

    UPDATE UserWallet SET balance = balance - p_amount, cashOut = cashOut + p_amount WHERE userWalletId = v_userWalletId;

    COMMIT;
    SELECT 0 AS code;

END ;;
DELIMITER ;