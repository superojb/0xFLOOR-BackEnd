DROP procedure IF EXISTS `Order_GetList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `Order_GetList`(
    p_userId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT O.orderId, O.orderName, OS.name AS status, SUM(B.price) AS price, O.createTime FROM `Order` AS O
    LEFT JOIN OrderStatus AS OS ON O.orderStatusId = OS.orderStatusId
    INNER JOIN (
        SELECT O.orderId, (OI.price * OI.num) AS price FROM `Order` AS O
        LEFT JOIN OrderItem AS OI ON O.orderId = OI.orderId
        WHERE userId = p_userId
    ) AS B ON O.orderId = B.orderId GROUP BY O.orderId;

END ;;
DELIMITER ;