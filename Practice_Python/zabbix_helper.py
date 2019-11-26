from pyzabbix import ZabbixAPI
import xlwt
import pandas as pd
import os
import platform

projectName= 'qqq'
if platform.system() == 'Windows':
    SRC = "C:\\Users\\eric.zhai\\Desktop\\{}".format(projectName)
    DEST = "C:\\Users\\eric.zhai\\Desktop\\{}-new".format(projectName)
    srcExists = os.path.exists(SRC)
    destExists = os.path.exists(DEST)
    if not srcExists:
        os.makedirs(SRC)
    if not destExists:
        os.makedirs(DEST)
else:
    SRC='/tmp/{}'.format(projectName)
    DEST='/tmp/{}-new'.format(projectName)
    srcExists = os.path.exists(SRC)
    destExists = os.path.exists(DEST)
    if not srcExists:
        os.makedirs(SRC)
    if not destExists:
        os.makedirs(DEST)


class pyZabbixApi(object):
    def __init__(self):
        self.user = 'Admin'
        self.password = 'zabbix'

    def login(self):
        zapi = ZabbixAPI("http://10.xx.12.192/zabbix")
        zapi.login(self.user, self.password)
        return zapi

    def getGroupIdByName(self, zapi, group_name):
        groups = zapi.hostgroup.get(output='extend')
        for group in groups:
            if group['name'] == group_name:
                return group['groupid']

    def getHostsFromGroupId(self, zapi, group_id):
        hosts = zapi.host.get(groupids=group_id, output=['hostid', 'host', 'name'])
        return hosts

    def getItemAndTrigerFromHost(self, zapi, hosts):
        '''
        oneHostData:存储一台主机的信息
        oneItemTriData：存储一条含有触发器的监控项信息
        oneItemData：存储一条监控项信息
        oneTriData:一条触发器信息
        '''
        for host in hosts:
            items = zapi.item.get(hostids=host['hostid'],
                                  output=['name', 'key_'])
            #存储主机List
            oneHostData = list()
            oneHostData.append(['主机IP', '监控项ID', '监控项描述', '监控项键值', '触发器ID', '触发器表达式',
                           '触发器描述', '告警等级','触发器停用与否'])
            for item in items:
                triggers = zapi.trigger.get(itemids=item['itemid'], output=['expression',
                                                                               'description',
                                                                               'priority','status'],expandExpression='True')
                #存储一条含有触发器的监控项
                oneItemTriData = list()
                oneItemTriData.append(host['host'])
                #存储一条监控项
                oneItemData = list()
                oneItemData.extend(list(item.values()))

                for trigger in triggers:
                    oneTriData = list(trigger.values())
                    oneItemTriDataTemp = oneItemTriData.copy()
                    oneItemDataTemp = oneItemData.copy()
                    oneItemDataTemp.extend(oneTriData)
                    oneItemTriDataTemp.extend(oneItemDataTemp)
                    oneHostData.append(oneItemTriDataTemp)
            write_in_excel(oneHostData)

def write_in_excel(result):
    global SRC
    try:
        book = xlwt.Workbook()
        sheet = book.add_sheet(result[1][0])
        for row in range(len(result)):
            for col in range(len(result[0])):
                sheet.write(row, col, result[row][col])
        if platform.system() == 'Windows':
            book.save(SRC + '\\' + '{}.xls'.format(result[1][0]))
        else:
            book.save(SRC + '/' + '{}.xls'.format(result[1][0]))
    except  IndexError:
        print('no trigger')

def formatExcel(filepath):
    global DEST
    df=pd.read_excel(filepath)

    # 去除监控项键值列中的基础监控项
    df = df[~ df['监控项键值'].str.contains('agent.hostname', case=False)]
    df = df[~ df['监控项键值'].str.contains('agent.ping', case=False)]
    df = df[~ df['监控项键值'].str.contains('agent.version', case=False)]
    df = df[~ df['监控项键值'].str.contains('proc.num\[,,run\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('proc.num\[\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.cpu.load\[all,avg1\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.cpu.num', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.cpu.load\[all,avg5\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.cpu.util\[,idle\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.cpu.util\[,iowait\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.hostname', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.uname', case=False)]
    df = df[~ df['监控项键值'].str.contains('system.uptime', case=False)]
    df = df[~ df['监控项键值'].str.contains('vfs', case=False)]
    df = df[~ df['监控项键值'].str.contains('vm.memory.size\[available\]', case=False)]
    df = df[~ df['监控项键值'].str.contains('kernel.maxfiles', case=False)]
    df = df[~ df['监控项键值'].str.contains('kernel.maxproc', case=False)]

    #去除已停用的触发器
    df=df[~df['触发器停用与否'].isin([1])]
    #去除无用列
    df = df.drop(['监控项ID'],axis=1)
    df = df.drop(['触发器ID'],axis=1)
    df = df.drop(['触发器停用与否'],axis=1)
    # print(df)
    if platform.system() == 'Windows':
        fileName = filepath.split("\\")
        df.to_excel(DEST + '\\' + 'new-' + fileName[-1])
    else:
        fileName = filepath.split("/")
        df.to_excel(DEST + '/' + 'new-' + fileName[-1])


if __name__=='__main__':
    #zabbix组名
    zabbixGroupName = 'test'
    projectName = 'qqq'
    r = pyZabbixApi()
    zapi = r.login()
    group_id = r.getGroupIdByName(zapi, '{}'.format(zabbixGroupName))
    hosts = r.getHostsFromGroupId(zapi,group_id)
    r.getItemAndTrigerFromHost(zapi,hosts)

    src = "C:\\Users\\eric.zhai\\Desktop\\{}".format(projectName)
    if platform.system() == 'Windows':
        src = "C:\\Users\\eric.zhai\\Desktop\\{}".format(projectName)
    else:
        src = '/tmp/{}'.format(projectName)

    files = os.listdir(src)
    for file in files:
        filepath = os.path.join(src,file)
        formatExcel(filepath)
