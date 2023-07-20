DROP procedure IF EXISTS `Order_CheckTimeout`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `Order_CheckTimeout`(
)
/**

 */
label:BEGIN
    DECLARE v_Cancelled_orderStatusId INT DEFAULT (SELECT orderStatusId FROM OrderStatus WHERE name = '已取消');
    DECLARE v_unpaid_orderStatusId INT DEFAULT (SELECT orderStatusId FROM OrderStatus WHERE name = '未支付');

    -- 未支付超過八小時則自動取消訂單
    UPDATE `Order` SET orderStatusId = v_Cancelled_orderStatusId, note = CONCAT(note, '| 支付超時，自動取消訂單')
    WHERE orderStatusId = v_unpaid_orderStatusId AND createTime < DATE_SUB(NOW(), INTERVAL 8 MINUTE);
    COMMIT;

END ;;
DELIMITER ;