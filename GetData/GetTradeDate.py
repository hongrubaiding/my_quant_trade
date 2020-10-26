# -- coding: utf-8 --

'''
获取回测期间所有调仓日
'''

from PrintInfo import PrintInfo

class GetTradeDate:
    def __init__(self,get_API):
        self.get_API = get_API
        self.PrintInfoDemo = PrintInfo()

    def get_trade_date(self,start_date='2019-01-01',end_date='2020-01-01',method='month_1'):
        '''
        获取起止日期内的所有调仓日
        :param method: month_1，每月的第一个交易日
        :return:
        '''
        result_list=[]
        if method=='month_1':
            dic_date = self.get_API.THS_DateQuery(exchange='SSE', params='dateType:0,period:M,dateFormat:0', begintime=start_date, endtime=end_date)
            if dic_date['errorcode']!=0:
                self.PrintInfoDemo.print_info('INFO','获取持仓日期错误，错误代码%s'%dic_date['errorcode'])
            else:
                date_list = dic_date['tables']['time']
                for date_str in date_list:
                    target_date = self.get_API.THS_DateOffset('SSE', 'dateType:0,period:D,offset:1,dateFormat:0,output:singledate', date_str)
                    result_list.append(target_date['tables']['time'][0])
        return result_list



if __name__=="__main__":
    import iFinDPy as THSIfind
    THSIfind.THS_iFinDLogin(username='zszq5366', password='114155')
    GetTradeDateDemo =GetTradeDate(get_API=THSIfind)
    GetTradeDateDemo.get_trade_date()