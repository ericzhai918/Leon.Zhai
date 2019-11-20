import pandas as pd

def zabbix_csv_format_to_excel(filepath):

    df=pd.read_csv(filepath,error_bad_lines=False)

    #查看触发器ID列
    #print(df['触发器ID'])

    #去除触发器ID列中的空值
    df = df.dropna(subset=['触发器ID'])

    #去除监控项键值列中的基础监控项
    df=df[~ df['监控项键值'].str.contains('agent', case=False)]
    df=df[~ df['监控项键值'].str.contains('net.tcp', case=False)]
    #df=df[~ df['监控项键值'].str.contains('proc.num', case=False)]
    df=df[~ df['监控项键值'].str.contains('kernel', case=False)]
    df=df[~ df['监控项键值'].str.contains('system', case=False)]
    df=df[~ df['监控项键值'].str.contains('vm', case=False)]
    df=df[~ df['监控项键值'].str.contains('vfs', case=False)]

    #去除已停用的触发器
    df=df[~df['触发器停用与否'].isin([1])]

    #有空值的列都删除（删除有多个触发器）
    df.dropna(axis=1,how='any')

    #去除无用列
    df = df.drop(['监控项ID'],axis=1)
    df = df.drop(['触发器ID'],axis=1)
    df = df.drop(['触发器停用与否'],axis=1)
    df = df.drop(['监控项键值'],axis=1)

    df.to_excel('test.xlsx')

if __name__ == '__main__':
    filepath = 'C:\\Users\\eric.zhai\\Desktop\\gls_测试.csv'
    zabbix_csv_format_to_excel(filepath)

