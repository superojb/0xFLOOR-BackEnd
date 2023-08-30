DROP procedure IF EXISTS `User_GetWalletList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `User_GetWalletList`(
    p_UserId INT(10),
    p_Limit INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有该用户
 */
label:BEGIN

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_UserId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;
    SELECT 0 AS code;

    DROP TEMPORARY TABLE IF EXISTS User_GetWalletList;
	CREATE TEMPORARY TABLE User_GetWalletList
    SELECT
        C.currencyId,
        C.name,
        C.nickname,
        C.imgUrl,
        C.color,
        UW.balance + UW.freeze + UW.cashOut + UW.thaw AS lumpSum
    FROM `0xFLOOR`.UserWallet AS UW
    INNER JOIN `0xFLOOR`.Currency AS C ON UW.currencyId = C.currencyId
    WHERE UW.userId = p_UserId;

    -- 如果一個幣也沒有則顯示USDT
    IF((SELECT COUNT(1) FROM User_GetWalletList) = 0) THEN
        SELECT currencyId, name, nickname, imgUrl, color, 0 AS lumpSum FROM `0xFLOOR`.Currency WHERE name = 'USDT' LIMIT 1;
    ELSE
        SELECT currencyId, name, nickname, imgUrl, color, lumpSum FROM User_GetWalletList ORDER BY -lumpSum LIMIT p_Limit;
    END IF ;
END ;;
DELIMITER ;