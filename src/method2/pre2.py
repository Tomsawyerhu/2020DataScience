import pandas as pd
from pandas import DataFrame

'''
根据contests文件夹下各场比赛的score.csv
汇总所有选定的比赛的题目id(带比赛的编号),score
写进pro.csv这一个文件    
'''

def get_pro(contests):
    df0=DataFrame({'id':[]})
    for contest_name in contests:
        df=pd.read_csv("contests\\"+contest_name+"\\score_"+contest_name+".csv")
        df0=pd.merge(df0,df,how='outer')
    df0.to_csv("pro.csv",index=False)

if __name__=='__main__':

    #contests=[3,6,9,10,13,14,15,16,18,23,24,25,26,31,32,36,37,38,40,44,45,46]
    #pre1.py选出的18场比赛
    contests = [3, 6, 9, 10, 13, 14, 15, 16, 18, 23, 26, 32, 36, 37, 40, 44, 45, 46]
    for i in range(len(contests)):
        if len(str(contests[i]))==1:
            contests[i]='agc00'+str(contests[i])
        else:
            contests[i]='agc0'+str(contests[i])
    print(contests)
    print(len(contests))#18

    get_pro(contests)