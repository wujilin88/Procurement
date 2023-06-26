import requests, json, time, xlwt
from bs4 import BeautifulSoup
#请求头
RHeaders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
#运行状态
runing = False
t = time.time()
Excel_head = {
    0: '序号',
    1: '采购项目名称',
    2: '采购需求概况',
    3: '预算金额（元）',
    4: '预计采购时间（填写到月）',
    5: '备注',
    6: '标题',
    7: '意向时间',
    8: '地址'
}
#列表URL
Url_category = "https://zfcg.czt.zj.gov.cn/portal/category"
#详情URL
Url_detail = "https://zfcg.czt.zj.gov.cn/portal/detail"


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
    req = requests.post(Url_category,json=request)
    reqdata = json.loads(req.text)
    #循环便利，将值存储到集合中
    for x in reqdata['result']['data']['data']:
        articleIds.append(x['articleId'])
    return articleIds
    pass
#111
#抓取列表详情信息
def Crawling_detail():
    articleIds = Crawling_category(request_head)
    req = requests.get(Url_detail+'?articleId='+articleIds[0])

    print(Url_detail+'?articleId='+articleIds[0])
    print(req.text)


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
    Crawling_detail()
    pass
