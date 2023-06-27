import requests, json, time, xlwt, warnings
from bs4 import BeautifulSoup

#处理错误警告
warnings.filterwarnings("ignore",category=DeprecationWarning)
#请求头
RHeaders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
#运行状态
runing = False

t = time.time()

Excel_head = {
    0: '序号',
    1: '项目市县',
    2: '采购项目名称',
    3: '采购需求概况',
    4: '发布时间',
    5: '中标方',
    6: '中标金额（万元）',
    7: '公告网址',
    8: '备注'
}

#列表URL
Url_category = "https://zfcg.czt.zj.gov.cn/portal/category"
#详情URL
Url_detail = "https://zfcg.czt.zj.gov.cn/portal/detail"

#预留，后面需要从页面上传过来
request_head = {
    "pageNo":"1",
    "pageSize":"15",
    "publishDateBegin":"null",
    "publishDateEnd":"null",
    "categoryCode":"110-188043",
    "excludeDistrictPrefix":"90",
    "_t":int(round(t * 1000))
}

#抓取列表信息id
def Crawling_category(request):
    #创建集合 用于存储详情列表id
    articleIds = []
    publishDates = []
    req = requests.post(Url_category,json=request)
    reqdata = json.loads(req.text)
    #循环便利，将值存储到集合中
    for x in reqdata['result']['data']['data']:
        articleIds.append(x['articleId'])
        publishDates.append(x['publishDate'])
    print(articleIds)
    print(publishDates)
    return articleIds

    pass


#抓取列表详情信息
def Crawling_detail():
    range = ''
    # articleIds = Crawling_category(request_head)
    #请求链接传参
    params = {
        'articleId' : 'BJJtiSSOk9bIKURn3bNEyg=='
    }
    req = requests.get(url=Url_detail, params=params, headers=RHeaders)
    reqdata = json.loads(req.text)
    print(reqdata)
    #获取招标信息中详细信息列表
    htmldata = reqdata['result']['data']['content']
    soup = BeautifulSoup(htmldata, features='lxml')
    tables = soup.findAll("table",{"class": "form-panel-input-cls"})
    #print(soup)
    #print(tables)
    for table in tables:
        # 用于判断是否为列表的第一列
        a = 0
        # 用于存储对应数据下标
        index = -1
        trs = table.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td")
            if a == 0:
                for i, td in enumerate(tds):
                    td_data = td.find(text=True)
                    if td_data == "服务范围" or td_data == '施工范围':
                        index = i
                        a = a + 1
                        break
            else:
                if index == -1:
                    range = "在列表中未能找到【范围范围】或者【施工范围】"
                    break
                else:
                    range = tds[index].find(text=True)

                pass

    #标题
    title = reqdata['result']['data']['title']
    #项目名称
    projectName = reqdata['result']['data']['projectName']
    datatime = reqdata

    # print(title)
    # print(projectName)
    # print(range)


    #trs = tables.findAll("tr")
    #设置下标初始值
    # index = 0
    # fwfwIndex = -1
    # for tds in trs:
    #     if index == 0:
    #         x = 0
    #         for td in tds:
    #             content = td.find(text=True)
    #             if content == '服务范围' or content == '施工范围':
    #                 fwfwIndex = x
    #             break
    #             x = x + 1
    #         continue
    #     else:
    #         if fwfwIndex == -1:
    #             break
    #         print(tds[fwfwIndex])
    #     index = index + 1


    #print(title,projectName)
    #print(Url_detail+'?articleId='+'BJJtiSSOk9bIKURn3bNEyg==')
    #print(req.text)


    pass


#生成excle
def Excle():
    work_book = xlwt.Workbook(encoding="UTF-8")
    worksheet = work_book.add_sheet("爬取数据")
    for i in Excel_head:
        worksheet.write(0,i,Excel_head[i])
    work_book.save("test.xlsx")

    pass

#程序停止
def Stop():
    runing = False
    pass



if __name__ == '__main__':
    # Crawling_category(request_head)
    Crawling_detail()
    pass
