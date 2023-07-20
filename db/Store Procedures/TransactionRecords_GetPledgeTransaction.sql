DROP procedure IF EXISTS `TransactionRecords_GetPledgeTransaction`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `TransactionRecords_GetPledgeTransaction`(
    p_MinerBindingId VARCHAR(200),
    p_userId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该机器
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT orderId FROM MinerBinding WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT
        transactionRecordsId,
        hax,
        currencyName
    FROM TransactionRecords
    WHERE initiationType = 0
      AND initiationAssociateId = p_MinerBindingId
      AND type = 2
      AND status = 0;

END ;;
DELIMITER ;