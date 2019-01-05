#爬取中小学数据库学校名称及详情页链接

from pandas import DataFrame;
from urllib.request import quote
#导入模块，需要先安装pandas，Dataframe等库，使用pip或pip3安装；
#获取时需要输入学校名称及地区及学校级别(初中高中等)，前两者需完全匹配，前者可部分匹配，例如学校“北京”，地区“北京”，级别“高中”；


school_name = input('请输入学校名称，可输入单个字符来匹配：')   #学校名称
address_name  = input('请输入地区名称，需完全正确：')  #地区名称
grade_name = input('请输入学级，例如"高中"等：')   #学级名称
Timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
#http://xuexiao.eol.cn/?cengci=%E9%AB%98%E4%B8%AD_cengci&keywords=%E5%8C%97%E4%BA%AC&local1=%E5%8C%97%E4%BA%AC_local1&local2=

#定义函数save，方便后续调用，主要用来保存爬取内容至csv文件；
def save(names,links):
    df = DataFrame({
        '学校名称': [names],
        '链接': [links]
    })
    df.to_csv(
        "~/Downloads/" + Timestamp + ".csv", mode='a', header=False
    )

#定义学校及链接打印函数，便于后续调用；
def print_school_name(url):
    #url = 'http://xuexiao.eol.cn/?cengci=' + quote(grade_name.encode('utf-8')) + '_cengci&keywords=' + quote(school_name.encode('utf-8')) + '&local1=' + quote(address_name.encode('utf-8')) + '_local1&local2='
    #搜索结果第一页；
    url = url
    res = requests.get(url).content.decode('utf-8')
    bsurl = bs4.BeautifulSoup(res,'html.parser')
    link = bsurl.select('.right_box a')
    for i in link:
        print(str(i.get('href')) + ' ' + str(i.get_text()))
        name = str(i.get_text())
        link = str(i.get('href'))
        save(name,link)


#定义翻页函数，便于爬取数据时翻页继续爬取，同时结合前两个函数同时运行；
def fanye(num):
    url = 'http://xuexiao.eol.cn/?cengci=' + quote(grade_name.encode('utf-8')) + '_cengci&keywords=' + quote(
        school_name.encode('utf-8')) + '&local1=' + quote(address_name.encode('utf-8')) + '_local1&local2='
    print_school_name(url)
    list = requests.get(url).content.decode('utf-8')
    bslist = bs4.BeautifulSoup(list,'html.parser')
    page_num = bslist.select('.page font')
    num_list = page_num[0].get_text() #获取搜索的学校数量；
    num_page = round(int(num_list)//int(5)) + int(1)
    for i in range(1,num_page):
        url2 = 'http://xuexiao.eol.cn/?page=' + quote(str(i)) + '&amp;cengci=' + quote(grade_name.encode('utf-8')) + '_cengci&amp;local1=' + quote(school_name.encode('utf-8')) + '_local1&amp;keywords=' + quote(address_name.encode('utf-8'))
        print_school_name(url2)
        #save(str(i.get_text()),str(i.get('href')))

    #for x in range

fanye(1)