DROP procedure IF EXISTS `MiningMachine_GetDetails`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachine_GetDetails`(
    p_MinerBindingId VARCHAR(200),
    p_userId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该机器

    (1, '等待上链'),
    (2, '等待质押'),
    (3, '待激活'),
    (4, '準備工作中'),
    (5, '工作中'),
    (6, '已完成'),
    (7, '暂停中'),
    (8, '准备暂停中'),
    (9, '维修中'),
    (10, '等待支付维修费')
 */
label:BEGIN
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
        MinerBindingId,
        MB.miningMachineProductId,
        orderId,
        miningStatusId,
        MB.pledgeProfitRatioId,
        electricity,
        effectiveTime,
        TotalRevenue,
        workingDay,
        CONCAT(
            '[', CM.name, '|', C.name, ']',
            MM.name,
            '(', MMS.specification, '/', IF(CP.day = 0, '永久', CONCAT(CP.day, '天')), ')'
            ) AS Name,
        PPR.PledgeNum,
        PPR.ProfitRatio,
        Currency.nickname AS Currency
    FROM MinerBinding AS MB
    LEFT JOIN MiningMachineProduct AS MMP ON MB.miningMachineProductId = MMP.id
    INNER JOIN Combo AS C on MMP.comboId = C.id
    LEFT JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    LEFT JOIN ComboModel AS CM ON MMP.comboModelId = CM.id
    LEFT JOIN MiningMachineSpecification AS MMS ON MMP.miningMachineSpecificationId = MMS.id
    LEFT JOIN MiningMachine AS MM ON MMS.miningMachineId = MM.id
    LEFT JOIN PledgeProfitRatio AS PPR ON MB.pledgeProfitRatioId = PPR.pledgeProfitRatioId
    LEFT JOIN Currency ON Currency.currencyId = C.currencyId
    WHERE MB.MinerBindingId = p_MinerBindingId AND MB.userId = p_userId;

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