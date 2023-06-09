DROP procedure IF EXISTS `MiningMachineProduct_GetList`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachineProduct_GetList`(
    p_currencyId BIGINT(20)
)
/**
  code = 0 = OK
  code = 1 = 没有该货币
 */
label:BEGIN
    IF NOT EXISTS(SELECT currencyId FROM Currency WHERE currencyId = p_currencyId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    DROP TEMPORARY TABLE IF EXISTS MiningMachineProduct_List;
    CREATE TEMPORARY TABLE MiningMachineProduct_List
    SELECT
        C.id AS comboId,
        C.name AS comboName,
        CP.id AS comboPeriodId,
        IF(CP.day = 0, '永久', CONCAT(CP.day, '天')) AS period,
        CM.id AS comboModelId,
        CM.name AS comboModelName,
        MMS.id AS miningMachineSpecificationId,
        MMS.specification,
        MM.id AS miningMachineId,
        MM.name,
        MMP.id AS miningMachineProductId,
        MMP.price
    FROM Combo AS C
    LEFT JOIN MiningMachineProduct AS MMP ON C.id = MMP.comboId
    LEFT JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    LEFT JOIN ComboModel AS CM ON MMP.comboModelId = CM.id
    LEFT JOIN MiningMachineSpecification AS MMS ON MMP.miningMachineSpecificationId = MMS.id
    LEFT JOIN MiningMachine AS MM ON MMS.miningMachineId = MM.id
    WHERE C.currencyId = p_currencyId;

    -- 套餐
    SELECT comboId, ANY_VALUE(comboName) AS comboName FROM MiningMachineProduct_List GROUP BY comboId;

    -- 套餐模式
    SELECT comboModelId, ANY_VALUE(comboModelName) AS comboModelName  FROM MiningMachineProduct_List GROUP BY comboModelId;

    -- 套餐周期
    SELECT comboPeriodId, ANY_VALUE(period) AS period  FROM MiningMachineProduct_List GROUP BY comboPeriodId;

    -- 矿机规格
    SELECT miningMachineSpecificationId, ANY_VALUE(specification) AS specification
    FROM MiningMachineProduct_List GROUP BY miningMachineSpecificationId;

    -- 矿机
    SELECT miningMachineId, ANY_VALUE(name) AS name
    FROM MiningMachineProduct_List GROUP BY miningMachineId;

    -- 产品
    SELECT
        miningMachineProductId,
        miningMachineId,
        comboId,
        comboModelId,
        comboPeriodId,
        miningMachineSpecificationId,
        price
    FROM MiningMachineProduct_List ORDER BY miningMachineSpecificationId;

END ;;
DELIMITER ;
