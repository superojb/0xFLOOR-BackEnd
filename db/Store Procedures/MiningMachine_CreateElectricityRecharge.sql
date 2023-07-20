DROP procedure IF EXISTS `MiningMachine_CreateElectricityRecharge`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachine_CreateElectricityRecharge`(
    p_userId INT(10),
    p_minerBindingId VARCHAR(200),
    p_Num INT
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该机器
  code = 3 = 充值电力不可大于有效期
 */
label:BEGIN
    DECLARE v_OrderId VARCHAR(200);
    DECLARE v_OrderName VARCHAR(200) DEFAULT CONCAT(p_Num, '天电费');
    DECLARE v_electricity INT(10);
    DECLARE v_powerConsumption DOUBLE;
    DECLARE v_effectiveTime INT(10);
    DECLARE v_unpaid_orderStatusId INT DEFAULT (SELECT orderStatusId FROM OrderStatus WHERE name = '未支付' LIMIT 1);
    DECLARE v_ElectricityBill DOUBLE DEFAULT (SELECT CONVERT(value, DOUBLE) FROM MiningMachineSetting WHERE `key` = 'ElectricityBill' LIMIT 1);

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT orderId FROM MinerBinding WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT
        electricity,
        effectiveTime,
        MMP.powerConsumption,
        CONCAT(
            '[', MB.MinerBindingId, ']',
            MM.name,
            '(', MMS.specification, '/', IF(CP.day = 0, '永久', CONCAT(CP.day, '天')), ')',
            ' ', v_OrderName
            ) AS Name
    INTO
        v_electricity,
        v_effectiveTime,
        v_powerConsumption,
        v_OrderName
    FROM MinerBinding AS MB
    LEFT JOIN MiningMachineProduct AS MMP ON MB.miningMachineProductId = MMP.id
    INNER JOIN Combo AS C on MMP.comboId = C.id
    LEFT JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    LEFT JOIN ComboModel AS CM ON MMP.comboModelId = CM.id
    LEFT JOIN MiningMachineSpecification AS MMS ON MMP.miningMachineSpecificationId = MMS.id
    LEFT JOIN MiningMachine AS MM ON MMS.miningMachineId = MM.id
    LEFT JOIN PledgeProfitRatio AS PPR ON MB.pledgeProfitRatioId = PPR.pledgeProfitRatioId
    LEFT JOIN Currency ON Currency.currencyId = PPR.currencyId
    WHERE MB.MinerBindingId = p_MinerBindingId AND MB.userId = p_userId;

    IF v_effectiveTime != -999 AND p_num > (v_effectiveTime - v_electricity) THEN
        SELECT 3 AS code;
        LEAVE label;
    END IF ;

    SET v_OrderId = Order_CreateId(p_userId);
    INSERT `Order` (orderId, orderName, userId, orderStatusId, createTime, note, type)
    VALUE (v_OrderId, v_OrderName, p_userId, v_unpaid_orderStatusId, NOW(), '充值电力', 2);

    INSERT OrderItem (orderId, productId, productTypeId, price, num, initiationAssociateId)
    VALUE (v_OrderId, 1, 2, v_ElectricityBill * v_powerConsumption, p_Num, p_minerBindingId);

    COMMIT;
    SELECT 0 AS code;

    SELECT v_OrderId AS OrderId;

END ;;
DELIMITER ;