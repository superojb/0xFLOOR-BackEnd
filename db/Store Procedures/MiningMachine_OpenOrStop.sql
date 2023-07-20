DROP procedure IF EXISTS `MiningMachine_OpenOrStop`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `MiningMachine_OpenOrStop`(
    p_MinerBindingId VARCHAR(200),
    p_userId INT(10),
    p_IsOpen BOOLEAN
)
/**
  code = 0 = OK
  code = 1 = 没有用户
  code = 2 = 没有该机器
  code = 3 = 不可轉變狀態

    (1, '等待上链'),
    (2, '等待质押'),
    (3, '待激活'),
    (4, '準備工作中'),
    (5, '工作中'),
    (6, '已完成'),
    (7, '暂停中'),
    (8, '准备暂停中'),
    (9, '维修中'),
    (10, '等待支付维修费')
 */
label:BEGIN
    DECLARE v_miningStatusId INT;
    DECLARE v_minerAccount VARCHAR(200);
    DECLARE v_PledgeNum VARCHAR(200);
    DECLARE v_TransactionRecords_Type VARCHAR(200);
    DECLARE v_TransactionRecords_Status VARCHAR(200);

    IF NOT EXISTS(SELECT id FROM auth_user WHERE id = p_userId) THEN
        SELECT 1 AS code, 0 AS status;
        LEAVE label;
    END IF ;

    IF NOT EXISTS(SELECT orderId FROM MinerBinding WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId) THEN
        SELECT 2 AS code, 0 AS status;
        LEAVE label;
    END IF ;

    SELECT
        miningStatusId,
        minerAccount
    INTO
        v_miningStatusId,
        v_minerAccount
    FROM MinerBinding WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;

    -- 開啟 礦機
    IF p_IsOpen THEN

        -- 如果礦機狀態為 準備暫停中 則可以直接轉為工作中
        IF v_miningStatusId = 8 THEN
            UPDATE MinerBinding SET miningStatusId = 5 , updateTime = NOW()
            WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
            COMMIT;
            SELECT 0 AS code, 5 AS status;
            LEAVE label;

         -- 如果礦機 為暫停中
        ELSEIF v_miningStatusId = 7 THEN
            SELECT
                PPR.PledgeNum,
                TR.type,
                TR.status
            INTO
                v_PledgeNum,
                v_TransactionRecords_Type,
                v_TransactionRecords_Status
            FROM MinerBinding AS MB
            INNER JOIN PledgeProfitRatio AS PPR ON MB.pledgeProfitRatioId = PPR.pledgeProfitRatioId
            LEFT JOIN TransactionRecords AS TR ON TR.initiationType = 0 AND TR.initiationAssociateId = MB.MinerBindingId
            WHERE MB.MinerBindingId = p_MinerBindingId AND MB.userId = p_userId
            ORDER BY -TR.createTime LIMIT 1;

            -- 机器账号为空， 并且质押数量为0， 转为等待上链
            IF v_minerAccount IS NULL AND v_PledgeNum = 0 THEN
                UPDATE MinerBinding SET miningStatusId = 1 , updateTime = NOW()
                WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
                COMMIT;
                SELECT 0 AS code, 1 AS status;

            -- 如果質押數量為0 則無需質押， 直接轉為待激活
            ELSEIF v_PledgeNum = 0 AND v_minerAccount IS NOT NULL THEN
                UPDATE MinerBinding SET miningStatusId = 3 , updateTime = NOW()
                WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
                COMMIT;
                SELECT 0 AS code, 3 AS status;

            -- 檢查最新的質押記錄 是已經質押, 但机器账号为空， 转为等待上链
            ELSEIF v_TransactionRecords_Type = 2 AND v_TransactionRecords_Status = 1 AND v_minerAccount IS NULL THEN
                UPDATE MinerBinding SET miningStatusId = 1 , updateTime = NOW()
                WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
                COMMIT;
                SELECT 0 AS code, 1 AS status;

            -- 檢查最新的質押記錄 是已經質押, 但机器账号不为空， 转为待激活
            ELSEIF v_TransactionRecords_Type = 2 AND v_TransactionRecords_Status = 1 AND v_minerAccount IS NOT NULL THEN
                UPDATE MinerBinding SET miningStatusId = 3 , updateTime = NOW()
                WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
                COMMIT;
                SELECT 0 AS code, 3 AS status;

            -- 其他则都转为 等待质押
            ELSE
                UPDATE MinerBinding SET miningStatusId = 2 , updateTime = NOW()
                WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
                COMMIT;
                SELECT 0 AS code, 2 AS status;
            END IF;

        -- 其他則報錯
        ELSE
            SELECT 3 AS code, 0 AS status;
        END IF;

    -- 暫停礦機
    ELSE
        -- 如果礦機狀態為 工作中 則直接轉為準備暫停中
        IF v_miningStatusId = 5 THEN
            UPDATE MinerBinding SET miningStatusId = 8 , updateTime = NOW()
            WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
            COMMIT;
            SELECT 0 AS code, 8 AS status;

        -- 如果礦機狀態為 【等待上链, 準備工作中，等待质押， 待激活】 則可以直接轉為暫停中
        ELSEIF v_miningStatusId = 1 OR v_miningStatusId = 4 OR v_miningStatusId = 3 OR v_miningStatusId = 2 THEN
            UPDATE MinerBinding SET miningStatusId = 7 , updateTime = NOW()
            WHERE MinerBindingId = p_MinerBindingId AND userId = p_userId;
            COMMIT;
            SELECT 0 AS code, 7 AS status;

        -- 其他則報錯
        ELSE
            SELECT 3 AS code, 0 AS status;
        END IF;

    END IF;
END ;;
DELIMITER ;