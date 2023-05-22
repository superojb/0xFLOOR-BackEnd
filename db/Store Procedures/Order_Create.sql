DROP procedure IF EXISTS `Order_Create`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `Order_Create`(
    p_userId INT(10),
    p_orderName CHAR(200),
    p_revenueAddressId INT(10),
    p_ItemIdList TEXT,
    p_ItemNumList TEXT,
    p_ItemTypeList TEXT
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 错误的产品
  code = 3 = 产品数量不可为小于1
  code = 4 = 沒有該收益地址
 */
label:BEGIN
    DECLARE v_OrderId VARCHAR(200);
    DECLARE v_ItemId INT(10);
    DECLARE v_ItemNum INT(10);
    DECLARE v_ItemType INT(10);
    DECLARE v_Num INT(10) DEFAULT LENGTH(p_ItemIdList)-LENGTH(REPLACE(p_ItemIdList,',',''));
    DECLARE v_i INT(10) DEFAULT 0;

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT id FROM RevenueAddress WHERE id = p_revenueAddressId AND userId = p_userId) THEN
        SELECT 4 AS code;
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

    INSERT `Order` (orderId, orderName, userId, orderStatusId, createTime)
    VALUE (v_OrderId, p_orderName, p_userId, 1, NOW());

    -- 添加产品进入订单
    SET v_i = 0;
    REPEAT
        SET v_ItemId = SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemIdList,',',v_i+1),',',-1);
        SET v_ItemNum = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemNumList,',',v_i+1),',',-1) AS SIGNED);
        SET v_ItemType = SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemTypeList,',',v_i+1),',',-1);

        IF v_ItemType = 1 THEN
            INSERT OrderItem (orderId, productId, productTypeId, price, num)
            SELECT v_OrderId, v_ItemId, v_ItemType, price, v_ItemNum FROM MiningMachineProduct WHERE id = v_ItemId;

        -- 电费暂时硬核编码
        ELSEIF v_ItemType = 2 THEN
            INSERT OrderItem (orderId, productId, productTypeId, price, num)
            SELECT v_OrderId, v_ItemId, v_ItemType, value, v_ItemNum FROM MiningMachineSetting WHERE `key` = 'ElectricityBill' LIMIT 1;
        END IF;

        SET v_i = v_i+1;
    UNTIL v_i>v_Num END REPEAT;

    -- 綁定收益地址
    INSERT OrderRevenueBind (orderId, revenueAddressId, createTime)
    VALUE (v_OrderId, p_revenueAddressId, NOW());

    COMMIT;
    SELECT 0 AS code;
END ;;
DELIMITER ;