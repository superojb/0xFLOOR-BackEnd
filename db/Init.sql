CREATE DATABASE 0xFLOOR;

set global log_bin_trust_function_creators=1;

-- 无需质押
INSERT IGNORE PledgeProfitRatio (PledgeProfitRatioId, PledgeNum, ProfitRatio, currencyId)
VALUE (-999, 0, 100, -999),
(1, 0, 30, 1),
(2, 1, 40, 1),
(3, 10000, 70, 1);

-- 电费
INSERT MiningMachineSetting (miningMachineSettingId, `key`, value) VALUES
(1, 'ElectricityBill', '1');

INSERT IGNORE Currency (currencyId, name, staticIncome, status, imgUrl, nickname, ranking, color, exchangeRate, minimumWithdrawal) VALUES
(-999, '无', '', 0, '', '', -999, '', 0, 0),
(1, 'Phala', '0.114', 1, 'https://phala.subscan.io/static/img/phala.5cd02d2d.png', 'Phala', 1, 'D0FE53', 1, 10000),
(2, 'Bitcoin', '0.114', 1, 'https://i-cncdn.investing.com/crypto-logos/80x80/v1/bitcoin.png', 'BTC/BCH', 1, '', 1, 1),
(3, 'Phala', '0.114', 1, 'https://s2.coinmarketcap.com/static/img/coins/64x64/2280.png', 'FIL', 1, '', 1, 100),
(4, 'USDT', '0.114', 0, '', 'USDT', -100, '0DA88B', 1, 10);

INSERT IGNORE CurrencyNetwork (currencyNetworkId, name, status, currencyId) VALUES
(1, 'TRC20', 1, 4),
(2, 'Polkadot', 1, 1);

INSERT IGNORE OrderStatus (orderStatusId, name) VALUES
(1, '未支付'),
(2, '支付中'),
(3, '部分支付'),
(4, '处理中'),
(5, '订单已完成'),
(6, '已取消'),
(7, '已关闭'),
(8, '发生错误');

INSERT IGNORE Combo (id, name, currencyId) VALUES
(1, '比特小鹿', 1);

INSERT IGNORE ComboModel (id, name) VALUES
(1, '经典'),
(2, '加速');

INSERT IGNORE ComboPeriod (id, day) VALUES
(1, 30),
(2, 120),
(3, 0);

INSERT IGNORE MiningMachine (id, comboId, name) VALUES
(1, 1, '螞蟻礦機S19Pro套餐');

INSERT IGNORE MiningMachineSpecification (id, miningMachineId, specification) VALUES
(1, 1, '10TH/s'),
(2, 1, '50TH/s'),
(3, 1, '100TH/s'),
(4, 1, '200TH/s'),
(5, 1, '500TH/s');

INSERT IGNORE MiningMachineProduct
(comboId, comboPeriodId, comboModelId, miningMachineSpecificationId, price, fixedPrice, inventory, pledgeStatus, powerConsumption, quantitySold)
VALUES
(1, 3, 1, 1, 10, 10, 1, 1, 1, 1),
(1, 1, 1, 5, 10, 10, 1, 0, 2, 1);