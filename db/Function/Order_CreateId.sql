DROP FUNCTION IF EXISTS `Order_CreateId`;
DELIMITER ;
DELIMITER ;;
CREATE FUNCTION
    Order_CreateId(
        p_userId INT(10)
    )
    returns CHAR(200)
BEGIN
    DECLARE v_NowTime BIGINT(20) DEFAULT REPLACE(unix_timestamp(current_timestamp(3)),'.','');

    RETURN CONCAT(CONVERT(p_userId, CHAR ), CONVERT(v_NowTime, CHAR));
End;;
DELIMITER ;