DROP procedure IF EXISTS `UserCloudPowerList_MinerList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserCloudPowerList_MinerList`(
    p_UserId INT(10),
    p_currencyId INT(10)
)
/**
  code = 0 = OK
  code = 1 = 没有该用户
  code = 2 = 没有该货币
 */
label:BEGIN
    DECLARE v_AllTotalRevenue FLOAT DEFAULT 0;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_UserId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT currencyId FROM Currency WHERE currencyId = p_currencyId) THEN
        SELECT 2 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    DROP TEMPORARY TABLE IF EXISTS MinerList;
    CREATE TEMPORARY TABLE MinerList
    SELECT
        MB.MinerBindingId,
        MB.orderId,
        CONCAT(MM.name, '(', MMS.specification, '/', IF(CP.day = 0, '永久', CONCAT(CP.day, '天')), ')') AS name,
        MB.TotalRevenue AS output,
        MB.miningStatusId
    FROM MinerBinding AS MB
    LEFT JOIN MiningMachineProduct AS MMP ON MB.miningMachineProductId = MMP.id
    LEFT JOIN MiningMachineSpecification AS MMS ON MMP.miningMachineSpecificationId = MMS.id
    LEFT JOIN MiningMachine AS MM ON MMS.miningMachineId = MM.id
    LEFT JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    LEFT JOIN Combo AS C ON MMP.comboId = C.id
    WHERE MB.userId = p_UserId AND C.currencyId = p_currencyId
    ORDER BY MB.createTime DESC;

    SELECT
        MinerBindingId,
        orderId,
        name,
        output,
        miningStatusId
    FROM MinerList;

    SELECT SUM(output) INTO v_AllTotalRevenue FROM MinerList;

    SELECT
        SUM(MER.UserRevenue) AS previousAllTotalRevenue, v_AllTotalRevenue AS AllTotalRevenue
    FROM MinerEarningsRecords AS MER
    INNER JOIN MiningMachineProduct AS MMP ON MER.miningMachineProductId = MMP.id
    INNER JOIN Combo AS C ON MMP.comboId = C.id
    INNER JOIN Currency AS C2 ON C.currencyId = C2.currencyId
    WHERE C2.currencyId = p_currencyId AND MER.createTime = DATE_SUB(DATE(NOW()), INTERVAL 1 DAY) AND MER.userId = p_UserId;

END ;;
DELIMITER ;