# -- coding: utf-8 --

'''
因子有效性检验，回归分析
'''

from sklearn.linear_model import LinearRegression
import pandas as pd
import statsmodels.api as sm
import numpy as np

class FactorDetail:
    def __init__(self):
        pass

    def wash_none_df(self, facort_zdf_df,zdf_df, target_col_list, method='<0'):
        '''
        清理无意义数据,如市盈率小于零
        备注：结合method方法使用时，对不同因子（如大于零无意义的因子），应多次调用，改变method参数
        :param facort_zdf_df:
        :return:
        '''
        facort_df = facort_zdf_df.dropna(axis=0)
        target_zdf_df = zdf_df.dropna(axis=0)

        if method == '<0':
            target_set = set(facort_df.index.tolist())
            for col_name in target_col_list:
                target_set.intersection()
                target_set = target_set.intersection(set(facort_df[facort_df[col_name] >= 0].index.tolist()))
            target_df = facort_df.loc[list(target_set)]
            return target_df,target_zdf_df

    def get_standardize(self,factor_df):
        '''
        去除因子的极值,并标准化
        :param temp_df:
        :return:
        '''
        df_list = []
        for fac in factor_df.columns:
            #中位数去极值法
            temp_Se= factor_df[fac].copy()
            if fac == 'pe':
                temp_Se = 1/temp_Se

            factor_middle = temp_Se.median()
            MAD = (temp_Se - factor_middle).abs().median()
            limit_num = 3
            up_limit = factor_middle+limit_num*MAD
            down_limit = factor_middle-limit_num*MAD
            temp_Se[temp_Se>up_limit] = up_limit
            temp_Se[temp_Se<down_limit] = down_limit
            temp_Se.name = fac
            df_list.append(temp_Se)
        fac_df = pd.concat(df_list,axis=1,sort=True)

        #标准化,暂时未做市值加权
        result_df = (fac_df-fac_df.mean())/fac_df.std()
        result_df = pd.concat([result_df])
        return result_df

    def get_regression(self,fac_df,zdf_df,indus_size_df):
        dic_regression = {}
        x = fac_df.values.reshape(-1,1)
        c = np.ones((len(x),1))
        X = np.hstack((c,x))
        Y = zdf_df.values.reshape(-1,1)
        res = (sm.OLS(Y, X)).fit()
        dic_regression['R-squared'] = res.rsquared
        dic_regression['tvalues'] = res.tvalues[1]
        print(res.summary())
        return res

    def start_calc(self, facort_df,zdf_df,indus_size_df):
        '''
        因子数据计算主入口
        :param facort_df:
        :param zdf_df:
        :param indus_size_df:
        :return:
        '''
        #因子数据清洗
        wash_df,new_zdf_df = self.wash_none_df(facort_df, zdf_df,target_col_list=['pe'])
        #去极值、标准化
        fac_df= self.get_standardize(wash_df)
        total_index_list = list(set(fac_df.index.tolist()).intersection(set(new_zdf_df.index.tolist())))
        new_zdf_df = new_zdf_df.loc[total_index_list]
        fac_df = fac_df.loc[total_index_list]
        #回归分析
        self.get_regression(fac_df,new_zdf_df,indus_size_df)



if __name__ == '__main__':
    FactorDetailDemo = FactorDetail()
