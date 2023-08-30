DROP procedure IF EXISTS `UserWithdrawalAddress_GetList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWithdrawalAddress_GetList`(
    p_userId INT(10),
    p_currencyId INT(10),
    p_page INT,
    p_limit INT
)
/**
  code = 0 = OK
  code = 1 = User 不存在
  code = 2 = 该货币 不存在
  code = 3 = 该网络 不存在
  code = 4 = 该地址已存在

 */
label:BEGIN
    DECLARE v_skip INT DEFAULT (p_page - 1) * p_limit;
    DECLARE v_whereSQL VARCHAR(3000) DEFAULT CONCAT('WHERE 1=1 AND WA.userId = ', p_userId);
    DECLARE v_tempSQL VARCHAR(9000) DEFAULT '';

    IF p_currencyId IS NOT NULL THEN
        SET v_whereSQL := CONCAT(v_whereSQL, ' AND WA.currencyId = ', p_currencyId);
    END IF;

    SET v_tempSQL := CONCAT(
        'SELECT
            WA.id,
            WA.currencyId,
            WA.address,
            WA.notes,
            WA.currencyNetworkId,
            CN.name AS currencyNetworkName
        FROM WithdrawalAddress AS WA
        INNER JOIN CurrencyNetwork AS CN ON WA.currencyNetworkId = CN.currencyNetworkId ',
        v_whereSQL,
        ' LIMIT ',  v_skip, ', ', p_limit, ';'
        );

    SET @v_test := v_tempSQL;
    PREPARE stmt FROM @v_test;
	execute stmt;
	DEALLOCATE PREPARE stmt;


    SET v_tempSQL := CONCAT(
        'SELECT
            COUNT(1) AS totalCount
        FROM WithdrawalAddress AS WA ',
        v_whereSQL
    );
    SET @v_test := v_tempSQL;
    PREPARE stmt FROM @v_test;
	execute stmt;
	DEALLOCATE PREPARE stmt;

END ;;
DELIMITER ;