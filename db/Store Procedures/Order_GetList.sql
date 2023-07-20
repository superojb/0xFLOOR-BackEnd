DROP procedure IF EXISTS `Order_GetList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `Order_GetList`(
    p_userId INT,
    p_orderType INT,
    p_page INT,
    p_limit INT
)
/**
  code = 0 = OK
  code = 1 = 没有用户
 */
label:BEGIN
    DECLARE v_skip INT DEFAULT (p_page - 1) * p_limit;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    DROP TEMPORARY TABLE IF EXISTS TheOrderList;
    CREATE TEMPORARY TABLE TheOrderList
    SELECT O.orderId, O.orderName, OS.name AS status, SUM(B.price) AS price, O.createTime
    FROM `Order` AS O
    LEFT JOIN OrderStatus AS OS ON O.orderStatusId = OS.orderStatusId
    INNER JOIN (
        SELECT O.orderId, (OI.price * OI.num) AS price FROM `Order` AS O
        LEFT JOIN OrderItem AS OI ON O.orderId = OI.orderId
        WHERE userId = p_userId
    ) AS B ON O.orderId = B.orderId AND O.type = p_orderType GROUP BY O.orderId ORDER BY -ANY_VALUE(O.createTime);

    SELECT COUNT(orderId) AS totalRows FROM TheOrderList;
    SELECT orderId, orderName, status, price, createTime FROM TheOrderList
    LIMIT v_skip, p_limit ;

    DROP TEMPORARY TABLE IF EXISTS TheOrderList;
END ;;
DELIMITER ;