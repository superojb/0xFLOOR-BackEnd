DROP procedure IF EXISTS `OrderPaymentInfo_GetInfo`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `OrderPaymentInfo_GetInfo`(
    p_userId INT(10),
    p_OrderId VARCHAR(200)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 訂單錯誤
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT orderId FROM `Order` WHERE orderId = p_OrderId AND userId = p_userId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT A.orderId, A.status, A.price, A.createTime, UW.address, A.orderName FROM (
        SELECT O.orderId, OS.name AS status, SUM(B.price) AS price, O.createTime, O.userId, O.orderName
        FROM `Order` AS O
        LEFT JOIN OrderStatus AS OS ON O.orderStatusId = OS.orderStatusId
        LEFT JOIN (
            SELECT O.orderId, (OI.price * OI.num) AS price FROM `Order` AS O
            LEFT JOIN OrderItem AS OI ON O.orderId = OI.orderId
            WHERE userId = p_userId
        ) AS B ON O.orderId = B.orderId
        WHERE O.orderId = p_OrderId
        GROUP BY O.orderId
    ) AS A
    LEFT JOIN UserWallet AS UW ON A.userId = UW.userId AND UW.type = 1;
END ;;
DELIMITER ;