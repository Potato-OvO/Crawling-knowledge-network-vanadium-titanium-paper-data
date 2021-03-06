import requests
import re
import parsel
import csv

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

Base = declarative_base()


class ThesisURL(Base):
    __tablename__ = 'thesisURL'

    Index = Column(Integer, primary_key=True)
    url = Column(String(255))


engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/testurl")
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# 构造请求参数
url = 'https://kns.cnki.net/KNS8/Brief/GetGridTableHtml'
headers = {
    'Host': 'kns.cnki.net',
    'Origin': 'https://kns.cnki.net',
    'Referer': 'https://kns.cnki.net/kns8/defaultresult/index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}
SearchSql = []


def Parsed_pages(subject_name, num):
    """
    解析需要爬取的所有的href连接，传参给get_url()
    :return:
    """
    for i in range(1, num):
        print(f"正在获取第{i}页数据")
        if i == 1:
            data = {
                'IsSearch': 'true',
                'QueryJson': '{"Platform":"","DBCode":"SCDB","KuaKuCode":"CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CJFN,CCJD","QNode":{"QGroup":[{"Key":"Subject","Title":"","Logic":1,"Items":[{"Title":"主题","Name":"SU","Value":"' + subject_name + '","Operate":"%=","BlurType":""}],"ChildItems":[]}]}}',
                'PageName': 'DefaultResult',
                'DBCode': 'SCDB',
                'KuaKuCodes': 'CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CJFN,CCJD',
                'CurPage': '1',
                'RecordsCntPerPage': '20',
                'CurDisplayMode': 'listmode',
                'CurrSortField': '%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27)',
                'CurrSortFieldType': 'desc',
                'IsSentenceSearch': 'false',
                'Subject': '',
            }
            response = requests.post(url=url, headers=headers, data=data)
            datas = response.text
            selector = parsel.Selector(datas)
            a_list = selector.css('td.name a')
            search = selector.css('#sqlVal').css('::attr(value)').get()
            SearchSql.append(search)
            getUrl(a_list)
        else:
            data = {
                'IsSearch': 'false',
                'SearchSql': SearchSql[0],
                'QueryJson': '{"Platform":"","DBCode":"CFLS","KuaKuCode":"CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CCJD,CCVD,CJFN","QNode":{"QGroup":[{"Key":"Subject","Title":"","Logic":1,"Items":[{"Title":"主题","Name":"SU","Value":"' + subject_name + '","Operate":"%=","BlurType":""}],"ChildItems":[]}]}}',
                'PageName': 'defaultresult',
                'HandlerId': '11',
                'DBCode': 'CFLS',
                'KuaKuCodes': 'CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CCJD,CCVD,CJFN',
                'CurPage': str(i),
                'RecordsCntPerPage': '20',
                'CurDisplayMode': 'listmode',
                'CurrSortField': '',
                'CurrSortFieldType': 'desc',
                'IsSortSearch': 'false',
                'IsSentenceSearch': 'false',
                'Subject': '',
            }

            response = requests.post(url=url, headers=headers, data=data)
            datas = response.text
            selector = parsel.Selector(datas)
            a_list = selector.css('td.name a')
            getUrl(a_list)


def getUrl(a_list):
    """
    获取所有的url，保存到一个url_list列表
    :param a_list: 解析Parsed_pages（）传过来的a_list，并构成一个完整的url地址
    :return:
    """
    for hrefs in a_list:
        href = hrefs.css('::attr(href)').get()
        parameters = re.findall("/KNS8/Detail\?.*&FileName=(.*?)&DbName=(.*?)&DbCode=(.*?)&.*", href)
        try:
            parameter = parameters[0]
            filename = parameter[0]
            dbname = parameter[1]
            dbcode = parameter[2]
            url = "https://kns.cnki.net/kcms/detail/detail.aspx?" + "dbcode=" + dbcode + "&dbname=" + dbname + "&filename=" + filename;
            print(url)
            thesisURL = ThesisURL(url=url)
            db_session.add(thesisURL)
            db_session.commit()
        except:
            print(parameters)


if __name__ == '__main__':
    subject_name = input("输入要查询的论文主题名：")
    num = int(input("输入爬取的页数（不要输入过多以免超出范围）："))
    Parsed_pages(subject_name, num)
