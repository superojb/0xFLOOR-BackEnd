DROP procedure IF EXISTS `UserWallet_ChangeFreeze`;
DELIMITER ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `UserWallet_ChangeFreeze`(
    p_transactionRecordsId INT(10)
)
/**
  code = 0 = OK
 */
label:BEGIN
    DECLARE v_type INT;
    DECLARE v_amount DOUBLE;
    DECLARE v_status INT;
    DECLARE v_userWalletId INT;

    SELECT
        TR.type,
        TR.status,
        TR.amount,
        UW.userWalletId
    INTO
        v_type,
        v_status,
        v_amount,
        v_userWalletId
    FROM TransactionRecords AS TR
    INNER JOIN MinerBinding AS MB ON MB.MinerBindingId = TR.initiationAssociateId
    INNER JOIN MiningMachineProduct AS MMP ON MB.miningMachineProductId = MMP.id
    INNER JOIN Combo AS C ON MMP.comboId = C.id
    INNER JOIN UserWallet AS UW ON MB.userId = UW.userId AND C.currencyId = UW.currencyId
    WHERE transactionRecordsId = p_transactionRecordsId;

    -- 质押 and 已确认
    IF v_type = 2 AND v_status = 1 THEN
        UPDATE UserWallet SET freeze = freeze + v_amount WHERE userWalletId = v_userWalletId;
        COMMIT;
    END IF;

    COMMIT;
    SELECT 0 AS code;
END ;;
DELIMITER ;