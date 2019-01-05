# 爬取西刺代理ip及其他信息并保存至csv文件

from pandas import DataFrame
from urllib.request import quote


Timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))   #获取当前时间
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

#定义保存函数；
def save(ip,port,adress,hide,types,survive,verifica):
    df = DataFrame({
        'ip地址': [ip],
        '端口': [port],
        'ip地区': [adress],
        '是否匿名': [hide],
        'ip类型': [types],
        'ip存活时间': [survive],
        'ip验证时间': [verifica]
    })
    df.to_csv(
        "~/Downloads/" + Timestamp + ".csv", mode='a', header=False
    )


#定义翻页函数；
def fanye(num):
    a = 0
    while a < (num//100 + int(1)):
        a = a + 1
        url = 'https://www.xicidaili.com/nn/' + str(a)
        res = requests.get(url, headers=headers, timeout=5).content.decode('utf-8')
        bs4_res = bs4.BeautifulSoup(res, 'html.parser')
        print('正在获取' + url + '链接的ip信息；')
        time.sleep(3)
        #print(bs4_res)
        for i in range(1,101):
            ip = bs4_res.select('table tr')[i]
            bs4_ip = bs4.BeautifulSoup(str(ip),'html.parser')
            ip_source = bs4_ip.select('td')
            ip_num = ip_source[1].getText()  #ip地址
            ip_port = ip_source[2].getText()  #ip端口
            ip_adress = ip_source[3].getText()  #ip地区
            ip_hide = ip_source[4].getText()  #ip是否匿名
            ip_types = ip_source[5].getText()  #ip类型
            #ip_speed = ip_source[6].getText()  #ip速度
            #ip_connect_time = ip_source[7].getText() #ip连接时间
            ip_Survive_time = ip_source[8].getText() #ip存活时间
            ip_verification_time = ip_source[9].getText()  #验证时间
            print(ip_num + ':' + ip_port + ':' + ip_adress + ':' + ip_hide + ':' + ip_types + ':' + ip_Survive_time + ':' + ip_verification_time)
            save(ip_num, ip_port, ip_adress, ip_hide, ip_types, ip_Survive_time, ip_verification_time)
            time.sleep(1)

fanye(int(input('请输入需要获取多少IP，输入100的倍数：')))