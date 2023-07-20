DROP procedure IF EXISTS `MiningMachine_AddElectricity`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachine_AddElectricity`(
    p_orderId VARCHAR(200)
)
/**
  code = 0 = OK
  code = 4 = 没有订单
  code = 4 = 订单未支付
 */
label:BEGIN
    DECLARE v_orderId VARCHAR(200) DEFAULT 'NULL';
    DECLARE v_MinerBindingId VARCHAR(200);
    DECLARE v_electricity INT;
    DECLARE v_orderStatus INT;
    DECLARE v_Paid_orderStatusId INT DEFAULT (SELECT orderStatusId FROM OrderStatus WHERE name = '订单已完成' LIMIT 1);

    SELECT
        orderId,
        orderStatusId
    INTO
        v_orderId,
        v_orderStatus
    FROM `Order` WHERE orderId = p_orderId;

    IF v_orderId = 'NULL' THEN
        SELECT 4 AS code;
        LEAVE label;
    END IF ;

    IF v_orderStatus != v_Paid_orderStatusId THEN
        SELECT 5 AS code;
        LEAVE label;
    END IF ;

    SELECT
        initiationAssociateId,
        num
    INTO
        v_MinerBindingId,
        v_electricity
    FROM OrderItem WHERE orderId = p_orderId AND initiationAssociateId != 0;

    UPDATE MinerBinding SET electricity = electricity + v_electricity, updateTime = NOW() WHERE MinerBindingId = v_MinerBindingId;
    COMMIT;
    SELECT 0 AS code;
    LEAVE label;
END ;;
DELIMITER ;