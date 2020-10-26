# -- coding: utf-8 --

'''
初始化股票池入口
'''
from PrintInfo import PrintInfo
import pandas as pd

class GetInitStockBool():
    def __init__(self, get_API):
        self.PrintInfoDemo = PrintInfo()
        self.start_proess = True
        self.get_API = get_API
        if isinstance(self.get_API,bool):
            self.start_proess = False
            self.PrintInfoDemo.print_info('ERROR', '账号登录失败，程序停止！' )

    def get_stock_bool(self, code_bool, get_date='2020-10-15'):
        '''
        获取指定日期初始股票池
        :param code_bool: 板块ID，或者指定股票list
        :param get_date: 获取日期
        :return: dic_result，状态，股票列表
        '''
        dic_result = {}
        if not self.start_proess:
            dic_result['state'] = False
            return dic_result

        self.PrintInfoDemo.print_info('INFO','获取%s初始股票池...'%get_date)
        if isinstance(code_bool, list):
            dic_result['state'] = True
            dic_result['code_list'] = code_bool
            return dic_result

        param_str = '%s;%s' % (get_date, code_bool)
        code_bool_data = self.get_API.THS_DP(DataPoolname='block', paramname=param_str, FunOption='date:Y,thscode:Y,security_name:Y',)
        if code_bool_data.errorcode!=0:
            self.PrintInfoDemo.print_info('ERROR', '股票池获取失败，错误代码%s' % code_bool_data.errorcode)
            dic_result['state'] = False
            return dic_result
        code_bool_df = code_bool_data.data
        code_bool = code_bool_df['thscode'.upper()].tolist()
        self.PrintInfoDemo.print_info('INFO', '%s初始股票池获取成功' % get_date,code_bool)
        dic_result['state'] = True
        dic_result['code_list'] = code_bool
        return dic_result

    def get_stock_indus_size(self, code_list, date_str):
        '''
        获取股票行业属性,ths_the_sw_industry_stock申万
        :param code_list:
        :param date_str:
        :return:
        '''
        inus_df = pd.DataFrame()
        # THS_BD('300033.SZ,601878.SH', 'ths_the_sw_industry_stock;ths_mv_back_test_stock', '100,2020-10-16;2020-10-16')
        inus_data = self.get_API.THS_BD(code_list, 'ths_the_sw_industry_stock;ths_mv_back_test_stock', '100,%s;%s'% (date_str,date_str))
        if inus_data.errorcode != 0:
            self.PrintInfoDemo.print_info('ERROR', '获取%s单因子数据有误，错误代码%s' % inus_data.errorcode)
        else:
            inus_df = inus_data.data
            inus_df.set_index('thscode', inplace=True)
            inus_df.rename(columns={"ths_the_sw_industry_stock":"申万一级行业","ths_mv_back_test_stock":"总市值"},inplace=True)
        return inus_df



if __name__=='__main__':
    import iFinDPy as THSIfind
    THSIfind.THS_iFinDLogin(username='zszq5366', password='114155')
    GetInitStockBoolDemo = GetInitStockBool(THSIfind)
    GetInitStockBoolDemo.get_stock_indus_size(code_list=['300033.SZ','601878.SH','002673.SZ'],date_str='2020-10-09')
