DROP procedure IF EXISTS `UserWallet_GetUserWalletLogList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_GetUserWalletLogList`(
    p_userId INT(10),
    p_currencyId INT(10),
    p_type INT(10),
    p_page INT,
    p_limit INT
)
/**
  code = 0 = OK
 */
label:BEGIN
    DECLARE v_skip INT DEFAULT (p_page - 1) * p_limit;
    DECLARE v_whereSQL VARCHAR(3000) DEFAULT CONCAT('WHERE 1=1 AND UWL.userId = ', p_userId);
    DECLARE v_tempSQL VARCHAR(9000) DEFAULT '';

    IF p_currencyId IS NOT NULL THEN
        SET v_whereSQL := CONCAT(v_whereSQL, ' AND UWL.currencyId = ', p_currencyId);
    END IF;

    IF p_type IS NOT NULL THEN
        SET v_whereSQL := CONCAT(v_whereSQL, ' AND UWL.type = ', p_type);
    END IF;



    SET v_tempSQL := CONCAT(
        'SELECT
            C.currencyId,
            C.name,
            C.imgUrl AS logo,
            UWL.changeAmount,
            UWL.balance,
            UWL.hax,
            UWL.transactionTime,
            UWL.type,
            UWL.status
        FROM UserWalletLog AS UWL
        INNER JOIN Currency AS C ON UWL.currencyId = C.currencyId ',
        v_whereSQL,
        ' ORDER BY -UWL.transactionTime',
        ' LIMIT ',  v_skip, ', ', p_limit, ';'
        );

    SET @v_test := v_tempSQL;
    PREPARE stmt FROM @v_test;
	execute stmt;
	DEALLOCATE PREPARE stmt;


    SET v_tempSQL := CONCAT(
        'SELECT
            COUNT(1) AS totalCount
        FROM UserWalletLog AS UWL ',
        v_whereSQL
    );
    SET @v_test := v_tempSQL;
    PREPARE stmt FROM @v_test;
	execute stmt;
	DEALLOCATE PREPARE stmt;
END ;;
DELIMITER ;