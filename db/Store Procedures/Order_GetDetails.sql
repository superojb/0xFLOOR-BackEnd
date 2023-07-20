DROP procedure IF EXISTS `Order_GetDetails`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `Order_GetDetails`(
    p_orderId VARCHAR(200),
    p_userId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 4 = 没有该订单
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT orderId FROM `Order` WHERE orderId = p_orderId AND userId = p_userId) THEN
        SELECT 4 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT orderId, createTime, OS.name AS status, note AS `explain`
    FROM `Order` AS O
    INNER JOIN OrderStatus AS OS ON O.orderStatusId = OS.orderStatusId
    WHERE orderId = p_orderId;

    SELECT
        IF(O.productTypeId = 2 AND O.productId = 1, '电费', CONCAT(MM.name, '(', MMS.specification, 'x', IF(CP.day = 0, '永久', CONCAT(CP.day, '天')), ')')) AS name,
        IF(CP.day = 0, '永久', CONCAT(CP.day)) AS day,
        currency.nickname AS currency,
        O.num,
        O.price,
        O.initiationAssociateId
    FROM OrderItem AS O
    LEFT JOIN MiningMachineProduct AS MMP ON O.productId = MMP.id AND O.productTypeId = 1
    LEFT JOIN MiningMachineSpecification AS MMS ON MMP.miningMachineSpecificationId = MMS.id
    LEFT JOIN MiningMachine AS MM ON MMS.miningMachineId = MM.id
    LEFT JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    LEFT JOIN Combo AS C ON MMP.comboId = C.id
    LEFT JOIN ComboModel AS CM ON MMP.comboModelId = CM.id
    LEFT JOIN Currency AS currency ON C.currencyId = currency.currencyId WHERE O.orderId = p_orderId;

    SELECT
        OS.name AS OrderStatus,
        SUM(B.price) AS price,
        IF(OPI.type = 1, 'USDT(TRC20)', '未知') AS PaymentType,
        OPI.createTime,
        OPI.confirmationUrl
    FROM `Order` AS O
    LEFT JOIN OrderPaymentInfo AS OPI ON O.orderId = OPI.orderId
    INNER JOIN OrderStatus AS OS ON O.orderStatusId = OS.orderStatusId
    INNER JOIN (
        SELECT O.orderId, (OI.price * OI.num) AS price FROM `Order` AS O
        INNER JOIN OrderItem AS OI ON OI.orderId = p_orderId
        WHERE userId = p_userId AND O.orderId = p_orderId
    ) AS B ON O.orderId = p_orderId GROUP BY O.orderId;
END ;;
DELIMITER ;