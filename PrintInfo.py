# -- coding: utf-8 --

'''
日志信息打印
'''

from datetime import datetime

class PrintInfo:
    def __init__(self):
        pass

    def print_info(self,info_style='INFO',*args):
        time_str = datetime.now().strftime("%H-%M-%S")
        if len(args)==1:
            print(time_str + '【%s】:' % time_str, args[0])
        else:
            print(time_str + '【%s】:' % time_str, args[0],args[1:])

if __name__=="__main__":
    PrintInfoDemo = PrintInfo()
    PrintInfoDemo.print_info('INFO','23242342','234545')
