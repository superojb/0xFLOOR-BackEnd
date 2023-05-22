INSERT OrderStatus (orderStatusId, name) VALUES
(1, '未支付'),
(2, '支付中'),
(3, '部分支付'),
(4, '处理中'),
(5, '订单已完成'),
(6, '已取消'),
(7, '已关闭'),
(8, '发生错误');

INSERT Currency (id, name, staticIncome, status, imgUrl, nickname) VALUES
(1, 'Bitcoin', 0.0791, 1, 'https://www.bitdeer.com/cloud-mining/_nuxt/img/6a33374.png', 'BTC/BCH'),
(2, 'FilCoin', 0.063, 1, 'https://www.bitdeer.com/cloud-mining/_nuxt/img/ec29e27.png', 'FIL');

INSERT MiningMachineSetting (miningMachineSettingId, `key`, value) VALUES
(1, 'ElectricityBill', '1');

INSERT Combo (id, name, currencyId) VALUES
(1, '比特小鹿', 1);

INSERT ComboModel (id, name) VALUES
(1, '经典'),
(2, '加速');

INSERT ComboPeriod (id, day) VALUES
(1, 30),
(2, 120);

INSERT MiningMachine (id, comboId, name) VALUES
(1, 1, '螞蟻礦機S19Pro套餐');

INSERT MiningMachineSpecification (id, miningMachineId, specification) VALUES
(1, 1, '10TH/s'),
(2, 1, '50TH/s'),
(3, 1, '100TH/s'),
(4, 1, '200TH/s'),
(5, 1, '500TH/s');

INSERT MiningMachineProduct (id, comboId, comboPeriodId, comboModelId, miningMachineSpecificationId, price) VALUES
(1, 1, 1, 1, 1, 10),
(2, 1, 1, 1, 2, 12),
(3, 1, 2, 1, 4, 32),
(4, 1, 2, 1, 5, 52);
set global log_bin_trust_function_creators=1;