DROP procedure IF EXISTS `Order_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `Order_Create`(
    p_userId INT(10),
    p_orderName CHAR(200),
    p_ItemIdList TEXT,
    p_ItemNumList TEXT,
    p_ItemTypeList TEXT,
    p_pledgeProfitRatioId INT
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 错误的产品
  code = 3 = 产品数量不可为小于1
  code = 5 = 质押选择错误
 */
label:BEGIN
    DECLARE v_OrderId VARCHAR(200);
    DECLARE v_ItemId INT(10);
    DECLARE v_ItemNum INT(10);
    DECLARE v_ItemType INT(10);
    DECLARE v_Num INT(10) DEFAULT LENGTH(p_ItemIdList)-LENGTH(REPLACE(p_ItemIdList,',',''));
    DECLARE v_i INT(10) DEFAULT 0;
    DECLARE v_MiningMachineProductId INT(10);
    DECLARE v_MiningMachineProduct_price DECIMAL(5, 2);
    DECLARE v_MiningMachineProduct_powerConsumption DOUBLE;
    DECLARE v_pledgeStatus INT;
    DECLARE v_pledgeProfitRatioId INT;
    DECLARE v_currencyId INT;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    -- 检查是否有错误的产品
    REPEAT
        SET v_ItemId = SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemIdList,',',v_i+1),',',-1);
        SET v_ItemNum = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemNumList,',',v_i+1),',',-1) AS SIGNED);
        SET v_ItemType = SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemTypeList,',',v_i+1),',',-1);

        IF v_ItemType = 1 THEN
            IF NOT EXISTS(SELECT id FROM MiningMachineProduct WHERE id = v_ItemId) THEN
                SELECT 2 AS code;
                LEAVE label;
            END IF ;
        END IF;

        IF v_ItemNum < 1 THEN
            SELECT 3 AS code;
            LEAVE label;
        END IF;

        SET v_i = v_i+1;
    UNTIL v_i>v_Num END REPEAT;

    SET v_OrderId = Order_CreateId(p_userId);

    INSERT `Order` (orderId, orderName, userId, orderStatusId, createTime, note, type)
    VALUE (v_OrderId, p_orderName, p_userId, 1, NOW(), '', 1);

    -- 添加产品进入订单
    SET v_i = 0;
    REPEAT
        SET v_ItemId = SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemIdList,',',v_i+1),',',-1);
        SET v_ItemNum = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemNumList,',',v_i+1),',',-1) AS SIGNED);
        SET v_ItemType = SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemTypeList,',',v_i+1),',',-1);

        IF v_ItemType = 1 THEN
            SELECT
                MMP.id,
                MMP.price,
                MMP.powerConsumption,
                MMP.pledgeStatus,
                C.currencyId
            INTO
                v_MiningMachineProductId,
                v_MiningMachineProduct_price,
                v_MiningMachineProduct_powerConsumption,
                v_pledgeStatus,
                v_currencyId
            FROM MiningMachineProduct AS MMP
            INNER JOIN Combo AS C ON MMP.comboId = C.id
            WHERE MMP.id = v_ItemId;

            -- 不开启质押
            IF v_pledgeStatus = 0 THEN
                SET v_pledgeProfitRatioId = -999;
            ELSE
                -- 检查质押比例是否存在
                IF EXISTS(SELECT currencyId FROM PledgeProfitRatio WHERE pledgeProfitRatioId = p_pledgeProfitRatioId AND currencyId = v_currencyId) THEN
                    SET v_pledgeProfitRatioId = p_pledgeProfitRatioId;
                ELSE
                    SELECT 5 AS code;
                    LEAVE label;
                END IF;
            END IF;

            INSERT OrderItem (orderId, productId, productTypeId, price, num, initiationAssociateId)
            VALUE (v_OrderId, v_ItemId, v_ItemType, v_MiningMachineProduct_price, v_ItemNum, p_pledgeProfitRatioId);

        ELSEIF v_ItemType = 2 THEN
            INSERT OrderItem (orderId, productId, productTypeId, price, num, initiationAssociateId)
            SELECT v_OrderId, v_ItemId, v_ItemType, v_MiningMachineProduct_powerConsumption * value, v_ItemNum, 0
            FROM MiningMachineSetting WHERE `key` = 'ElectricityBill' LIMIT 1;
        END IF;

        SET v_i = v_i+1;
    UNTIL v_i>v_Num END REPEAT;

    COMMIT;
    SELECT 0 AS code;

    SELECT v_OrderId AS OrderId;
END ;;
DELIMITER ;