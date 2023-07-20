DROP procedure IF EXISTS `MiningMachine_GetPledgeInfo`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachine_GetPledgeInfo`(
    p_MinerBindingId VARCHAR(200),
    p_userId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该机器
 */
label:BEGIN
    DECLARE v_CurrencyName VARCHAR(200);
    DECLARE v_currencyId INT;
    DECLARE v_PledgeNum FLOAT;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT orderId FROM MinerBinding WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT
        Currency.name,
        Currency.currencyId,
        PPR.PledgeNum
    INTO
        v_CurrencyName,
        v_currencyId,
        v_PledgeNum
    FROM MinerBinding AS MB
    LEFT JOIN PledgeProfitRatio AS PPR ON MB.pledgeProfitRatioId = PPR.pledgeProfitRatioId
    LEFT JOIN Currency ON Currency.currencyId = PPR.currencyId
    WHERE MB.MinerBindingId = p_MinerBindingId AND MB.userId = p_userId;

    SELECT v_CurrencyName AS Currency, v_PledgeNum AS PledgeNum, v_currencyId AS currencyId;

    SELECT address FROM UserWallet WHERE currencyId = v_currencyId AND userId = p_userId;

    SELECT
        TR.type,
        TR.status,
        TR.coolingTime
    FROM MinerBinding AS MB
    INNER JOIN PledgeProfitRatio AS PPR ON MB.pledgeProfitRatioId = PPR.pledgeProfitRatioId
    INNER JOIN TransactionRecords AS TR ON TR.initiationType = 0 AND TR.initiationAssociateId = MB.MinerBindingId
    WHERE MB.MinerBindingId = p_MinerBindingId AND MB.userId = p_userId
    ORDER BY -TR.createTime LIMIT 1;

END ;;
DELIMITER ;