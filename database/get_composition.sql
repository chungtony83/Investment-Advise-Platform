
SELECT isin, exchangeid, symbol FROM hive.dwd2_test.equity_all WHERE isin IN (
SELECT isin FROM hive.dwd2_test.holding_detail 
    WHERE fundid IN 
        (SELECT fundid FROM hive.dwd2_test.fund_all WHERE isin IN ('US9229083632', 'US78467X1090', 'US46090E1038')))
        AND exchangeid IN ('NAS', 'NYS');


-- US9229083632: VOO
-- US78467X1090: DIA
-- US46090E1038: QQQ