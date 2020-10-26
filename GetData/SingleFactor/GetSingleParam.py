# -- coding: utf-8 --


'''
获取因子及其对应的参数
'''

class GetSingleParam:
    def __init__(self):
        self.total_factor = self.get_total_factor()

    def get_total_factor(self):
        pass

    def get_factor(self,factor_name='pe_ttm'):
        dic_result= {}
        dic_result['wind'] = 'pe_ttm'
        dic_result['ifind'] = 'ths_pe_ttm_stock'
        dic_result['zhongwen'] ='市盈率'
        dic_result['ind_name'] = 'pe'
        return dic_result



if __name__=='__main__':
    GetSingleParamDemo = GetSingleParam()
    GetSingleParamDemo.get_factor()