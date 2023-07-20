DROP procedure IF EXISTS `MinerBinding_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MinerBinding_Create`(
    p_orderId CHAR(200)
)
/**
  code = 0 = OK
  code = 1 = 没有该订单
 */
label:BEGIN
    -- 需要加多少个
    DECLARE v_ItemNum INT(10);
    DECLARE v_i INT(10);
    DECLARE v_ProductId INT(10);
    DECLARE v_UserId INT(10);
    DECLARE v_pledgeProfitRatioId INT;
    DECLARE v_miningStatusId INT;
    DECLARE v_PledgeNum DOUBLE;
    DECLARE v_ComboPeriod INT;
    DECLARE v_electricity INT;

    IF NOT EXISTS(SELECT orderId FROM `Order` WHERE orderId = p_orderId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT
        OI.productId, OI.num, O.userId, OI.initiationAssociateId, PPR.PledgeNum, IF(CP.day = 0, -999, CP.day)
    INTO
        v_ProductId, v_ItemNum, v_UserId, v_pledgeProfitRatioId, v_PledgeNum, v_ComboPeriod
    FROM OrderItem AS OI
    INNER JOIN `Order` AS O ON OI.orderId = O.orderId
    INNER JOIN PledgeProfitRatio AS PPR ON OI.initiationAssociateId = PPR.pledgeProfitRatioId
    INNER JOIN MiningMachineProduct AS MMP ON OI.productId = MMP.id
    INNER JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    WHERE OI.orderId = p_orderId AND OI.productTypeId = 1 LIMIT 1;

    SELECT
        num / v_ItemNum
    INTO
        v_electricity
    FROM OrderItem AS OI
    INNER JOIN `Order` AS O ON OI.orderId = O.orderId
    WHERE OI.orderId = p_orderId AND OI.productTypeId = 2 LIMIT 1;

    SET v_i = 1;
    REPEAT
        INSERT IGNORE MinerBinding
            (MinerBindingId, minerAccount, miningStatusId, createTime,
             updateTime, miningMachineProductId, orderId, userId, effectiveTime,
             electricity, pledgeProfitRatioId, TotalRevenue, workingDay)
        VALUE
            (CONCAT(p_orderId, '-', v_i), NULL, IF(v_PledgeNum = 0, 1, 2), NOW(),
             NOW(), v_ProductId, p_orderId, v_UserId, v_ComboPeriod,
            v_electricity, v_pledgeProfitRatioId, 0, 0);

        SET v_i = v_i+1;
    UNTIL v_i>v_ItemNum END REPEAT;

    COMMIT;
    SELECT 0 AS code;

END ;;
DELIMITER ;