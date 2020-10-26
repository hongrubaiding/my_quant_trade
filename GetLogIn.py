# -- coding: utf-8 --

'''
同花顺账号登录
'''

import iFinDPy as THSIfind
from PrintInfo import PrintInfo

class GetLogIn:
    def __init__(self):
        self.PrintInfoDemo = PrintInfo()

    def get_log(self):
        log_state = THSIfind.THS_iFinDLogin(username='zszq5366', password='114155')
        if log_state == 0:
            self.PrintInfoDemo.print_info('INFO', '登录同花顺API接口成功!')
            return THSIfind
        else:
            self.PrintInfoDemo.print_info('ERROR', '登录同花顺API接口失败，错误代码%s' % log_state)
            return False


if __name__ == '__main__':
    GetLogInDemo = GetLogIn()
    GetLogInDemo.get_log()
