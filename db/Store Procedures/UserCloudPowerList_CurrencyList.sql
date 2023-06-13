DROP procedure IF EXISTS `UserCloudPowerList_CurrencyList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserCloudPowerList_CurrencyList`(
    p_UserId INT(10)
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

    SELECT
        C.currencyId,
        ANY_VALUE(C.nickname) AS nickname,
        ANY_VALUE(C.imgUrl) AS imgUrl,
        IF(B.currencyId IS NULL, 0, CAST(SUM(B.currencyId) AS UNSIGNED )) AS num,
        ROUND(0.00000000, 8) AS totalOutput
    FROM Currency AS C
    LEFT JOIN (
        SELECT MB.MinerBindingId, C.currencyId FROM MinerBinding AS MB
        LEFT JOIN MiningMachineProduct AS MMP ON MB.miningMachineProductId = MMP.id
        LEFT JOIN Combo AS C ON MMP.comboId = C.id
        WHERE MB.userId = p_UserId
    ) AS B ON C.currencyId = B.currencyId
    WHERE C.status = 1
    GROUP BY C.currencyId;

END ;;
DELIMITER ;