import requests
import re
import parsel
import csv

# 构造请求参数
url = 'https://kns.cnki.net/KNS8/Brief/GetGridTableHtml'
headers = {
    'Host': 'kns.cnki.net',
    'Origin': 'https://kns.cnki.net',
    'Referer': 'https://kns.cnki.net/kns8/defaultresult/index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}
param = {
}
# url列表
url_list = []
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
                # 'CurrSortField': '%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27)',
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
                # 'SearchSql': '0645419CC2F0B23BC604FFC82ADF67C692F6944D0202D2DC6656A6C7AC1EDC809A155BF2DE12E2F98C4BD55B8DC0937B674DE0CD2B86BB3266824FC750BED96C00B6FFF8B53C732897B1E623A882A32F0BF5CF51B6EAB5042BB9034B07B74C7567AD9C4111D92A13DEE9BBC8802C0D282F61171EB1794B796728CBF9FEE654FB6C550FE2154E7B199FF2B0A2F14AFB850735D5697534FBB43620CC6627D49477153E142292C900AECEE9968C0C2D01B114E7D3A5C688C197F2D6353CEEA237DECD555EDDFE4641352CE4DE3CD5DB4ADF5126EB9AAB81EEB6A9C7048B3ABC508E2511FFECD5B809118E6FE24E065BDF56F8D679AD87AEC534278173EA90C7BD2F782DF316E0689F3F9CF7130A3D164C0B9F67E0BCFD40B11A893E059B385C139C93381B0E49D9B341E9F873F36CD7419DB9DCFAEE1BC089BBDD3F69BD336BCE0E0CB84C933EE6C249556E6F2832A7DBC426AC9B3FF7C49275C5C9A40BAEE1916D88FE3B89F46F3855840137991445DDDE36419A95CC34A3A67996D1066FC72587ECC3178EF9FE478D64E053B67FE75AF13E01C467EF6BB65CB74CBC667876B06414BBE808D9BFDE5C7B37665C52B788CE77B25BBF742357D34924C53618AAB0F1F923AD03D5C0AAD60B43CDF34DE9F2642F6432E1AE8588C458E5A4F89EA592507F2D75D75E5CFC0C5EC385E23CDDE479774AB9AA0C848545A87A13C88243D0F316BDD0D2D277F4156124D62AF5D1752EE9DF1AA61E73BD1851CA0CCBB0E643BBC465A5A252D0379F50BBCDD9057F7D9B5963318588BCA97EB74575AB118421EE8725A4E43DD27C107D64B1941DBCCB6E5126BC57C7E14BD5142219D1F0BCC312D76C5E166382E7A14D0D8212827A25ACD9BD083214B358CE6CF5DAD6A25B1B6D6513211C44E00F79B2862723CAC5828518BDDC3D1C4A4450501000B35D9173CD222F55DADD4BC7BB18D9AB47CE6299C5EC3F7B7BD795B65A1DB63746D7856CA667C6D0C28309D4176A54A771C8303BA11FC70D5FE03FE808B35150681CE1449249A6513EB94BE9DBE1002F0C41B2DC471CF1792524EDFEBC6BA3838E316B9FCF39E2F6DC7F08C6AF7C05DE1C44FD30BA2E7423256156E8E3E2030B10A42169A5A6517DDE5CBAFB12B19068053509B4AC822B1B0BDE93138A04D3ACF530960F2D0645FC754042DB1A5B6D47B6255DDF1B4EFBEB8598BAF2F25281C6F53AC1756AD3D5A1932C0E142E77B52816E4AC7D4D695E7C16419651FBB18A033CAFD61D21CF3D220CEB8FA651F61C8F54D64D8E0AA8E2B470BBCDA7EB3CAB4B8905896B2E40689132B955FA1C7E7E25B1BC9CC82A826EABF622883141F7E6F992AE351E603DC9099C61A8ADA1F7F65744F7DFDA26B8CDA8528B881CB36AAB7427BFB9ACDBC58C9C01F620563E58F62707CCAA39EE452D3D4759D5E3E3052DC349527AD8455515927D1624B17D63A6FE9752F9A4D826BBF1FE6914C3AA93F1C1549F085E831176639A0EED88137C4F23C7822354C331A44B4F6F54C1E955AAEB950DB3751C3805ACD1CA5547E3C802CF97860E1D3262F58535E6508D355402592BC37B1FA339A9F208F55EB8A1BF5345460CDBFD812E7C20499746B3454E3FF669A0C4B0B455EC008973C8F9AB9C80C5573318761584C171F3343F99EAAB0F3937384C698C14EE22C14B89B60C4B5C8F628C6A392294AC9E441117210C79D1DB69AF3F84337C0F4E1E688EDA21040754F8EEF70454821BCA70BF95C6E38042C2B85F4A903B893D15F3C0FABB5E9B8C0E444FD7A3577E686E77D59388393F41D13A39561DB31EB71B4E1CA6D16BFE4B9B75DBBB68C0B0F69A7EC7582418BE17199910F1613B8C5C7C4E76E2AC5179D82C535206BB5E47E94161F8CA30AD772C1C258FD2B8C4A4E336123DA420AA43C8CDE0A0CA25616D5253843D8909DB268E788E26AEA1773A9FA5AA423EE6084B4AD539A369647EAAC63F2F251AFCE25F802E9FDF730FE0DEF8CB1AE2A4CB7C8765A9C0D5A34C293E24B2ED5B6F555BDFDE462A8906553ED402C32CDCF30EC9AD44DB932153FEAAA0183DCA8A76F56FC69086D3DA8E7B7367A731E4526026A872F9BBD01EBBC9DEB838C4CBB9831C9289A1B2A546D2C90CCC08D122E0767534DDE37848728E2254ACC0DA2F0CFD9E0BE11195A916AF05C208AAB48C7DD6CEEE223A9E12E798412D2B20002A622011A1F4D1C596A5749D0136E8F60B7A2FBBB9864859EF1B9D68F2E09C03FDA1B5E4A6B32A3EFF0B9F0439F66A9DA8B18424142D930FDAA46FF733005F65353AAAA49CEB9E8994CC306A8A8FFDEF2ABA36EA78AC552DEE95415FD7FCFCFAB1066483C49461857A387980EF6C0B94AA6FFD7BD3EA49043310DFB5EC5681152027FAFEF2A1AE201380AC674E2E9D7B00C8F4508372A7ED7271DBEBE048ACCDBA191823D097890151A929453644F36784153280107D3CB2D96D798BF45C2F2C8F1BDD5D116F4862DDA8F7E0B6754DC57A6A7D5AAB7117600F8B11057E926B9B73D832340429651240801C1E3A7F32B393C522F9EFB385FDC3E946592DB9FBC81F5C468B897B5B809A36E09D89F1051426D4071D1A418AE57DF96C46F206F9DA5BABE48EA5E9EDFE4E034FBA8805E3D2C422295C2202060E407E7262AD57DFEA69D8A31E99D7FEEB0C166FFFE50E80231825D9D01732C8AEEC289B1E8679B2E989DCC38316C88893950119D4F4A5A77AA8B12698A740921DF4561AEC63049FC18688D70EA2C6E640C0316B2B8FF92A601A85F4A32E7FC97E05ED52A9B377E7BABC7E61E1D35798CEF5F21BEF45EA19F33A330B7293BDFCC608AAC7DB2F43E057196643CB251E4EAC5E56AE390C9CC58D30C6C668426DA477B1E61B4E6674A98B83B545004DC2511C1A72151AB1ACC1638C70E01D58',
                # 'SearchSql': '0645419CC2F0B23BC604FFC82ADF67C6E920108EDAD48468E8156BA693E89F481391D6F5096D7FFF3585B29E8209A884EFDF8EF1B43B4C7232E120D4832CCC896D30C069E762ACAB990E5EBAAD03C09721B4573440249365A4157D3C93DC874963F6078A465F9A4E6BEED14E5FD119B250F0488206491CF1C7F670020480B48EE2FF3341B3B9C8A0A38F9913EF596174EDD44BBA8277DA2BE793C92DF83782297DE55F70BBF92D5397159D64D1D3DAC96FAD28213BD3E1912A5B4A4AD58E5965CBDBA01069691140F14FD0298FBD1F452C7779EFF17124633292E356C88367122976245AA928FA07D061C0E091BB1136031750CD76D7D64E9D75B7FBAB11CAA5B80183AC60BB0885D2C0A0938C7D1F849656014326473DCB797D5D273C845DAF7FCE49D21478E9B06B77ADE6253ACD4FE1D87EE31B4B2C94E071EE733B3A64EA6EE9CD5F222FCD3DA1D83D9133EF8C9BED9ED3E55DA15F3B4A37C85463B60D2F0BEA46FC7135898D7D93F63AF8B2246716E32B699238901588EE5D1DEF30A01DCE9957CF6934E8B11E273747F9A9BB8ADF535E5E76F6A9386CFBE605748C132DA05E2D31832199B0A4ECF170ACA47154423CF6BBD9607FC505765E95637F93DC865AA738F5EE92B26DB9AF56509A5FC96FF9C3A1720633EBDDC62EC2162E7D5349CAC851ED0AD4E36DCF6FE25EBEAB42BF931DBE3CF4ED1A7BB8FD887C3C33D86B768B0BA7267C4E0E7DEE53D0931F71F07AE13BAFC46034A444EC24C7EA8F0086FAD197A8D2F18C6CBC5DF48050AF8D4C84DE03B9A6F1DF928D63286B1C924B7EC3BA8C2591D60491F95D271F0E7F02AA2AA93C3888B8CCEBB0414BD7145AD15A3166DB4860F85BC476B1B193C219EAE52E33E6BBC9B3AAAD97196977B7DABA36C04093ED723AD874EC6480477C6412B0F589DE6CC7D959855E41265213DCBB4D91238716DF38BF78C951259572F8E5968FAC5C5CDC006DBE919EEB5E5518F51162FCE7CDE520F60093D333FBE121D3164C6D2451F6431FB7973C659E6A9D287B545EC044DE2CBE170F3627719F8418D44E17987CEC7A89B52CB5525AF795DA892475ABF871C3A5A5FCBC5B03EB9BEC8598C8ADD7A68984BBBEF1244DD90386C05756687AB9D87A0B521319C093C3EC0D5EBEFDAB5459E29F1DA03D4C25DE740BF9FA2BC07DD510386E3BBE89F10D45513E29C8CF904763E723CE4BF2928D4DC2A731DD53595E9AACED90679FCDDACED022ECD59D72600A736D555A8B76BFE4CCD861E6A7F5A219EBE9A228BD008928299DB999D18F9CDD2E57E8C03EDF236E62EDB17A1FE5B023CF6E5A11892A5FA17EE5CFE348CA290DC691987A535223133D8CA101E8ABF13EFCAD929635E090B3C6BB6838E33B7C78C1DBA274101A6584300EF8D38C983AD544264217F6793562D19715CD711295C5410C72E88A64BD23D9049E5DF15EA6B3EB4473C1DDEBB416459322FEF0CC61D894476DCD62569527BE23FB7F66DF3F5182ABF2472FB60039CA77218F356D7F82E4EBAAA4C6875B5BD4729C81A29BDF55ED223AA0DAB04E1B248524FC504711360C330186327A780D6487BA831ABE55AAE38E69A0FBEF89D560E7AA26B991966E4B644338863E80AD9D1ACAD459EA933644C5A0D2EA44AD17205AED3BE66AEC01F48BA032EEBD620E2713082FE8D31E4A05A34F18BD389587FA4D3A9DFBB8C16AEE9C5FA9E667BA12A07B757D82F7BB41AC8867D9947CCBA3BB26381EC6D0D3966338DB6FA3D1A61F99A978C3B5ED2B31B7C14D54A4F688C4925C8AF99CB3EE3C2C06C7D35AD891BF0CFC820529FD990F2FF319BE195B1AD23C1667031C072EB1964F8512BB779125E46773C01714FCF0E339AEB0C44FB91B896A7A95AF4F81EB49006B570BC03ECA7D8DA45679F3B46A7AE3B46ED8D319CED49A3A5881A37CD3770703BDF026ACEF7D8662F85AFDBDD36C540FD419E18F30EA0483D24350B7C34C43F3D0065F339EAC15749DF8849F3880378FEA4AD7CCBAA827C828A5CAF7D56E97A87A3FAEEAE136B35FB37E8CE0233D9AF8DEABD47BD5B36A1B42B995D4F96FE744A2E25E9B6107801CACCA0DDC2B7ED5BFD39F68AB2E2BB66AB8286061049F3B5FFE871FFA520A7C0EEE3DEDF417D078DF9013B5F5251A07AE3D4D00B9AF1560200CC981D0E8BE17C9CE204C21E5E543C9E55421D4FCE2C309C68D376E3787AB4640FA99B82988A288FD22A2E0C9225E39A5DAA7EBEB0376912C9CA255A7AE49F3C5AB262B4FFFBA98A9548623C16D0C97C7315DF5FFD1507102EAA730E5247F1C492D49A45121347CFF39A5181729F1D33F28FA48035CBC02CF87DAF72067D70B524421AB21FF137A2C7AB2F90DAD1BA1786C16728E7B78DB0461B5B1E8CF7B88E765E67AF4E458EF3A5125D90DA88CE97D9AB9C4363E4A7D6B7F3B0420B93FEDF72248E076EC0871EDFC5744AC6F9F591CEC4CE3E0E681E1C1B21AFCC5BF5B22116F7E7A3ABA561F68F8AE685DA926756CD70C0E6057C7737537F972F8942CCFD073400F0D5C23F107F55FC07745ED334FB97130860A0B7B0B5B4B2B23417EA63C65BAF1624254BBA167373F1D6C0E0BB5A67F92008CFCA4F24276E725FD05802F94A5CC7E52CC005017C58A8757BDEDED54538DA513E975DFCDC7D3FA95552E960ABA05EB7C33CA37CCA1C93DFF13A493174A9BB3228118E0F2AEBBAEE074D557B6FA6000F0E5C73D563BB8E3598B4D8E94DDCAFEB5BBCDF74D39CCC8AD27A5D3C0CAB59D171D03EFF1C9129392939E2580257FCEA55859AEE4B88DCB2472D0598AA1E07F84ADA3F1ED185FAF33E81C730C6F9DD2C4E6BDABCDE3029325EA410F7D5810B6E31820F8C13B9850731A4938340082ED13F5B4240DBFFF3E050E3177641895D7044EF979459304B0B4911632A5CEDF0FDE677490ECFBE1B1',
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
            url_list.append(url)
        except:
            print(parameters)


def saveUrl():
    """
    钒钛url地址的保存
    :return:
    """
    with open("url地址.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["钒钛论文地址"])
        writer.writeheader()
        for i in range(len(url_list)):
            writer.writerow({"钒钛论文地址": url_list[i]})


def vanadiumTitaniumDownload():
    """
    钒钛pdf下载
    :return:
    """
    """.btn-dlpdf a::attr(href)"""
    for i in range(len(url_list)):
        datas = requests.get(url_list[i])


def readCsvList():
    with open('钒钛url地址.csv', 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        items = [item for item in reader]
        items = list(items)
        items.pop(0)
        print(items)
        print(len(items))


if __name__ == '__main__':
    subject_name = input("输入要查询的论文主题名：")
    num = int(input("输入爬取的页数（不要输入过多以免超出范围）："))
    Parsed_pages(subject_name, num)
    print("完整的url列表为:", url_list)
    saveUrl()
    # readCsvList()