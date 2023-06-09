DROP procedure IF EXISTS `MiningMachineProduct_GetProduct`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachineProduct_GetProduct`(
    p_productId BIGINT(20)
)
/**
  code = 0 = OK
  code = 1 = 没有该产品
 */
label:BEGIN
    IF NOT EXISTS(SELECT id FROM MiningMachineProduct WHERE id = p_productId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    SELECT 0 AS code;

    SELECT
        MMP.id AS miningMachineProductId,
        C.name AS comboName,
        IF(CP.day = 0, '永久', CONCAT(CP.day, '天')) AS period,
        CM.name AS comboModelName,
        MMS.specification,
        MM.name,
        MMP.price,
        MMSetting.value AS ElectricityBill
    FROM MiningMachineProduct AS MMP
    LEFT JOIN Combo AS C ON C.id = MMP.comboId
    LEFT JOIN ComboPeriod AS CP ON MMP.comboPeriodId = CP.id
    LEFT JOIN ComboModel AS CM ON MMP.comboModelId = CM.id
    LEFT JOIN MiningMachineSpecification AS MMS ON MMP.miningMachineSpecificationId = MMS.id
    LEFT JOIN MiningMachine AS MM ON MMS.miningMachineId = MM.id
    JOIN MiningMachineSetting AS MMSetting ON MMSetting.key = 'ElectricityBill'
    WHERE MMP.id = p_productId;

END ;;
DELIMITER ;
