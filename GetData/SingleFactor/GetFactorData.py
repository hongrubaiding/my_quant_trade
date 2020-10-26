# -- coding: utf-8 --

'''
获取因子数据、股票涨跌幅数据
'''
from PrintInfo import PrintInfo
import pandas as pd


class GetFactorData:
    def __init__(self, get_API):
        self.PrintInfoDemo = PrintInfo()
        self.get_API = get_API

    def get_main(self, last_date, trade_date, dic_factor_info, code_list):
        factor_df = pd.DataFrame()
        code_zdf_df = pd.DataFrame()
        self.PrintInfoDemo.print_info('INFO', '获取%s单因子%s数据' % (last_date, dic_factor_info['zhongwen']))
        factor_data = self.get_API.THS_BD(thsCode=code_list, indicatorName=dic_factor_info['ifind'],
                                          paramOption='%s,100' % last_date)
        if factor_data.errorcode != 0:
            self.PrintInfoDemo.print_info('ERROR', '获取%s单因子数据有误，错误代码%s' % factor_data.errorcode)
        else:
            factor_df = factor_data.data
            factor_df.set_index('thscode', inplace=True)
            factor_df.rename(columns={dic_factor_info['ifind']: dic_factor_info['ind_name']}, inplace=True)

            self.PrintInfoDemo.print_info('INFO', '获取%s股票池涨跌幅数据' % trade_date)
            code_zdf_data = self.get_API.THS_BD(thsCode=code_list, indicatorName='ths_chg_ratio_m_stock',
                                                paramOption='%s,100' % trade_date)
            code_zdf_df = code_zdf_data.data
            code_zdf_df.set_index('thscode', inplace=True)
            code_zdf_df.rename(columns={'ths_chg_ratio_m_stock': 'zdf'}, inplace=True)
            result_df = pd.concat([factor_df, code_zdf_df], axis=1, sort=True)
        return factor_df, code_zdf_df


if __name__ == "__main__":
    import iFinDPy as THSIfind
    THSIfind.THS_iFinDLogin(username='zszq5366', password='114155')
    GetFactorDataDemo = GetFactorData(get_API=THSIfind)
    GetFactorDataDemo.get_main()
