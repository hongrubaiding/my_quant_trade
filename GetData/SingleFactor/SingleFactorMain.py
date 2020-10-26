# -- coding: utf-8 --

'''
单因子有效性检验主入口
'''
from GetData.SingleFactor.GetSingleParam import GetSingleParam
from GetLogIn import GetLogIn
from GetData.GetTradeDate import GetTradeDate
from PrintInfo import PrintInfo

from GetInitStockBool import GetInitStockBool
from GetData.SingleFactor.GetFactorData import GetFactorData
from FactorCheck.FactorDetail import FactorDetail
from datetime import datetime, timedelta


class SingleFactorMain:
    def __init__(self):
        #账号登录
        GetLogInDemo = GetLogIn()
        self.get_API = GetLogInDemo.get_log()
        self.PrintInfoDemo = PrintInfo()

    def get_init_back_info(self):
        '''
        初始化回测信息,
        回测起止日期、股票池、调仓日
        :return:
        '''
        self.back_start_date = '2019-01-01'  # 回测开始时间
        self.back_end_date = '2020-01-01'  # 回测截止时间
        self.code_bool = '001005260'    #上证50
        GetTradeDateDemo = GetTradeDate(get_API=self.get_API)
        self.total_back_date = GetTradeDateDemo.get_trade_date(start_date=self.back_start_date,end_date=self.back_end_date)

    def start_back_stratety(self, dic_factor_info):
        '''
        开始回测
        :param dic_factor_info: 因子信息
        :return:
        '''
        self.get_init_back_info()
        if not self.total_back_date:
            return

        GetInitStockBoolDemo= GetInitStockBool(get_API=self.get_API)
        GetFactorDataDemo = GetFactorData(get_API=self.get_API)
        FactorDetailDemo = FactorDetail()
        for trade_str in self.total_back_date[1:]:
            last_date = self.total_back_date[self.total_back_date.index(trade_str)-1]   #上月初
            dic_code_bool = GetInitStockBoolDemo.get_stock_bool(code_bool=self.code_bool,get_date=last_date)
            indus_size_df = GetInitStockBoolDemo.get_stock_indus_size(code_list=dic_code_bool['code_list'],date_str=last_date)
            if not dic_code_bool['state']:
                return
            facort_df,zdf_df = GetFactorDataDemo.get_main(last_date,trade_str,dic_factor_info,code_list=dic_code_bool['code_list'])
            if facort_df.empty:
                return
            FactorDetailDemo.start_calc(facort_df,zdf_df,indus_size_df)



    def get_main(self):
        #主入口
        factor_name = 'pe_ttm'
        GetSingleParamDemo = GetSingleParam()
        dic_factor_info = GetSingleParamDemo.get_factor(factor_name=factor_name)
        self.start_back_stratety(dic_factor_info)


if __name__ == '__main__':
    SingleFactorMainDemo = SingleFactorMain()
    SingleFactorMainDemo.get_main()
