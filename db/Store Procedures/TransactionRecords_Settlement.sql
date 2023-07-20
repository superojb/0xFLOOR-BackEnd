DROP procedure IF EXISTS `TransactionRecords_Settlement`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `TransactionRecords_Settlement`(
    p_MinerBindingId VARCHAR(200),
    p_state VARCHAR(200),
    p_revenue FLOAT
)
/**
 */
label:BEGIN
    DECLARE v_miningStatusId INT;
    DECLARE v_previousDay DATE DEFAULT DATE_SUB(DATE(NOW()), INTERVAL 1 DAY);
    DECLARE v_ProfitRatio FLOAT DEFAULT 1;
    DECLARE v_userRevenue FLOAT;
    DECLARE v_effectiveTime INT;
    DECLARE v_electricity INT;

    -- 查詢是否有該礦機， 並且狀態不是已完成
    IF NOT EXISTS(SELECT orderId FROM MinerBinding WHERE MinerBindingId = p_MinerBindingId AND miningStatusId != 6) THEN
        LEAVE label;
    END IF ;

    -- 已经结算的就不用了
    IF EXISTS(
        SELECT orderId FROM MinerEarningsRecords
        WHERE MinerBindingId = p_MinerBindingId AND createTime = DATE_FORMAT(DATE(NOW()), '%Y-%m-%d')) THEN
        LEAVE label;
    END IF;

    DROP TEMPORARY TABLE IF EXISTS TheMinerBinding;
    CREATE TEMPORARY TABLE TheMinerBinding
    SELECT
        minerAccount, miningStatusId, miningMachineProductId,
        userId, effectiveTime, electricity, pledgeProfitRatioId, orderId, C.currencyId
    FROM MinerBinding AS MB
    INNER JOIN MiningMachineProduct AS MMP ON MB.miningMachineProductId = MMP.id
    INNER JOIN Combo AS C ON C.id = MMP.comboId
    WHERE MinerBindingId = p_MinerBindingId;

    SELECT
        miningStatusId
    INTO
        v_miningStatusId
    FROM TheMinerBinding LIMIT 1;

    DROP TEMPORARY TABLE IF EXISTS PreviousMinerEarningsRecords;
    CREATE TEMPORARY TABLE PreviousMinerEarningsRecords
    SELECT
        MinerBindingId, minerAccount, MinerTotalRevenue
    FROM MinerEarningsRecords WHERE MinerBindingId = p_MinerBindingId AND createTime = v_previousDay;

    -- 礦機狀態
    SELECT
        miningStatusId,
        IF(effectiveTime = -999, -999, effectiveTime - 1),
        electricity - 1
    INTO
        v_miningStatusId,
        v_effectiveTime,
        v_electricity
    FROM TheMinerBinding LIMIT 1;

    -- 礦機收益比例
    SELECT
        PPR.ProfitRatio / 100
    INTO
        v_ProfitRatio
    FROM TheMinerBinding AS MB
    INNER JOIN PledgeProfitRatio AS PPR ON PPR.pledgeProfitRatioId != 0 AND MB.pledgeProfitRatioId = PPR.pledgeProfitRatioId
    LIMIT 1;

    -- 礦機在工作， 並且礦機狀態為準備工作中
    IF p_state = 'WorkerIdle' AND v_miningStatusId = 4 THEN
        INSERT MinerEarningsRecords
            (minerAccount, miningStatusId, MinerTotalRevenue,
             MinerRevenueToday, UserRevenue, electricity,
             effectiveTime, createTime, MinerBindingId,
             miningMachineProductId, orderId, pledgeProfitRatioId, userId)
        SELECT
            minerAccount, miningStatusId, p_revenue,
            p_revenue, 0, electricity, effectiveTime, NOW(),
            p_MinerBindingId, miningMachineProductId,
            orderId, pledgeProfitRatioId, userId
        FROM TheMinerBinding;

        UPDATE MinerBinding SET miningStatusId = 5, updateTime = NOW() WHERE MinerBindingId = p_MinerBindingId;

        COMMIT;

    -- 礦機在工作, 並且礦機狀態為工作中
    ELSEIF p_state = 'WorkerIdle' AND v_miningStatusId = 5 THEN
        SELECT
            (p_revenue - MinerTotalRevenue) * v_ProfitRatio
        INTO
            v_userRevenue
        FROM PreviousMinerEarningsRecords WHERE MinerBindingId = p_MinerBindingId;

        INSERT MinerEarningsRecords
            (minerAccount, miningStatusId, MinerTotalRevenue,
             MinerRevenueToday, UserRevenue, electricity,
             effectiveTime, createTime, MinerBindingId,
             miningMachineProductId, orderId, pledgeProfitRatioId, userId)
        SELECT
            MB.minerAccount,
            MB.miningStatusId,
            p_revenue,
            p_revenue - ER.MinerTotalRevenue,
            v_userRevenue,
            v_electricity,
            v_effectiveTime,
            NOW(),
            p_MinerBindingId,
            miningMachineProductId,
            orderId,
            pledgeProfitRatioId,
            userId
        FROM TheMinerBinding AS MB
        INNER JOIN PreviousMinerEarningsRecords AS ER ON ER.MinerBindingId = p_MinerBindingId;

        UPDATE UserWallet AS UW
        INNER JOIN TheMinerBinding AS MB ON UW.userId = MB.userId
        SET UW.balance = UW.balance + v_userRevenue WHERE UW.userId = MB.userId AND UW.currencyId = MB.currencyId;

        UPDATE MinerBinding
        SET
            TotalRevenue = TotalRevenue + v_userRevenue,
            electricity = electricity - 1,
            effectiveTime = IF(effectiveTime = -999, -999, effectiveTime - 1),
            workingDay = workingDay + 1,
            updateTime = NOW()
        WHERE MinerBindingId = p_MinerBindingId;

        COMMIT;

    END IF;

    -- 扣除電力和有效期
    IF v_miningStatusId = 5 THEN

        -- 當電力等於0 並且有效期大於0 或者 有效期為永久 更新礦機為 已暫停
        IF v_electricity = 0 AND (v_effectiveTime > 0 OR v_effectiveTime = -999) THEN
            UPDATE MinerBinding SET
            miningStatusId = 7, updateTime = NOW(), electricity = v_electricity, effectiveTime = v_effectiveTime
            WHERE MinerBindingId = p_MinerBindingId;

        -- 當電力等於0 並且有效期等於0 更新礦機為 已完成
        ELSEIF v_electricity = 0 AND v_effectiveTime = 0 THEN
            UPDATE MinerBinding SET
            miningStatusId = 6, updateTime = NOW(), electricity = v_electricity, effectiveTime = v_effectiveTime
            WHERE MinerBindingId = p_MinerBindingId;
        END IF;
    END IF;

    DROP TEMPORARY TABLE IF EXISTS TheMinerBinding;
    DROP TEMPORARY TABLE IF EXISTS PreviousMinerEarningsRecords;

END ;;
DELIMITER ;