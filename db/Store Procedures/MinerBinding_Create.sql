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

    IF NOT EXISTS(SELECT orderId FROM `Order` WHERE orderId = p_orderId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT
        OI.productId, OI.num, O.userId
    INTO
        v_ProductId, v_ItemNum, v_UserId
    FROM OrderItem AS OI
    LEFT JOIN `Order` AS O ON OI.orderId = O.orderId
    WHERE OI.orderId = p_orderId AND OI.productTypeId = 1;

    SET v_i = 0;
    REPEAT
        INSERT IGNORE MinerBinding
            (MinerBindingId, minerAccount, miningStatusId, createTime, updateTime, miningMachineProductId, orderId, userId)
        VALUE
            (CONCAT(p_orderId, '-', v_ItemNum), NULL, 1, NOW(), NOW(), v_ProductId, p_orderId, v_UserId);

        SET v_i = v_i+1;
    UNTIL v_i>v_ItemNum END REPEAT;

    COMMIT;
    SELECT 0 AS code;

END ;;
DELIMITER ;