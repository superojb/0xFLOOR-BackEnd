DROP procedure IF EXISTS `UserWithdrawalAddress_Delete`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWithdrawalAddress_Delete`(
    p_userId INT(10),
    p_WithdrawalAddressId INT(10)
)
/**
  code = 0 = OK
  code = 5 = 不是自己的提现地址

 */
label:BEGIN
    IF not EXISTS(SELECT id FROM WithdrawalAddress WHERE userId = p_userId AND id = p_WithdrawalAddressId) THEN
        SELECT 5 AS code;
        LEAVE label;
    END IF ;

    DELETE FROM WithdrawalAddress WHERE id = p_WithdrawalAddressId AND userId = p_userId;
    COMMIT;
    SELECT 0 AS code;
END ;;
DELIMITER ;