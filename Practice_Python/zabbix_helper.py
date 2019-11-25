from pyzabbix import ZabbixAPI
import xlwt

class pyZabbixApi(object):
    def __init__(self):
        self.user = 'Admin'
        self.password = 'zabbix'

    def login(self):
        zapi = ZabbixAPI("http://10.11.12.192/zabbix")
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
        for host in hosts:
            items = zapi.item.get(hostids=host['hostid'],
                                  output=['name', 'key_'])
            onedata = list()
            onedata.append(['主机IP', '监控项ID', '监控项描述', '监控项键值', '触发器ID', '触发器表达式',
                           '触发器描述', '告警等级','触发器停用与否'])
            for item in items:
                triggers = zapi.trigger.get(itemids=item['itemid'], output=['expression',
                                                                               'description',
                                                                               'priority','status'],expandExpression='True')

                data = list()
                data.append(host['host'])
                dataTemp = list()
                dataTemp.extend(list(item.values()))

                for trigger in triggers:
                    trigger_data = list(trigger.values())
                    dataTemp.extend(trigger_data)
                    data.extend(dataTemp)
                    onedata.append(data)
            print(onedata)
            write_in_excel(onedata)

def write_in_excel(result):
    try:
        book = xlwt.Workbook()
        sheet = book.add_sheet(result[1][0])
        for row in range(len(result)):
            for col in range(len(result[0])):
                sheet.write(row, col, result[row][col])
        book.save('{}.xls'.format(result[1][0]))
    except  IndexError:
        print('这个机器没有触发器，请确认')


if __name__=='__main__':
    r = pyZabbixApi()
    zapi = r.login()
    group_id = r.getGroupIdByName(zapi, 'Onebank 性能测试 ZP 卡前置')
    hosts = r.getHostsFromGroupId(zapi,group_id)
    r.getItemAndTrigerFromHost(zapi,hosts)






# a = [1,2,3]
# b = [[4,4,4],[2,2,2]]
# data = list()
# d= list()
# d.extend(a)
#
# for i in b:
#     d1 = d.copy()
#     f= list(i)
#     d1.extend(f)
#     data.append(d1)
#     continue
#
# print(data)