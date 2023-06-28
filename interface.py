import requests, json, time, xlwt, warnings
from bs4 import BeautifulSoup

# 处理错误警告
warnings.filterwarnings("ignore", category=DeprecationWarning)
# 请求头
RHeaders = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

t = time.time()

# excel表头数据
Excel_head = {
    0: '序号',
    1: '项目市县',
    2: '采购项目名称',
    3: '采购需求概况',
    4: '发布时间',
    5: '中标金额（万元）',
    6: '中标方',
    7: '公告网址',
    8: '备注'
}

# 列表URL
Url_category = "https://zfcg.czt.zj.gov.cn/portal/category"
# 详情URL
Url_detail = "https://zfcg.czt.zj.gov.cn/portal/detail"
# 页面展示URL
Url_web = "https://zfcg.czt.zj.gov.cn/luban/detail"

# 预留，后面需要从页面上传过来
request_head = {
    "pageNo": "1",
    "pageSize": "15",
    "publishDateBegin": "null",
    "publishDateEnd": "null",
    "categoryCode": "110-188043",
    "excludeDistrictPrefix": "90",
    "_t": int(round(t * 1000))
}


# 抓取列表信息id
def crawlingCategory(request):
    # 创建集合 用于存储详情列表id
    articleIds = []
    req = requests.post(Url_category, json=request)
    reqdata = json.loads(req.text)
    # 循环便利，将值存储到集合中
    for x in reqdata['result']['data']['data']:
        articleIds.append(x['articleId'])
    return articleIds
    pass


# 抓取列表详情信息
def crawlingDetail(articleId):
    range = ''
    inviteName = ''
    price_text = ''
    supplier_text = ''
    # articleIds = Crawling_category(request_head)
    # 请求链接传参
    params = {
        'articleId': articleId
    }
    req = requests.get(url=Url_detail, params=params, headers=RHeaders)
    reqdata = json.loads(req.text)
    # 获取招标信息中详细信息列表
    htmldata = reqdata['result']['data']['content']
    soup = BeautifulSoup(htmldata, features='lxml')
    # 中标表格信息
    bidders = soup.findAll("table", {"class": "template-bookmark"})
    # 标书具体信息
    tables = soup.findAll("table", {"class": "form-panel-input-cls"})
    # 招标采购人名称信息
    name = soup.find("span", {"class": "code-00014"})
    if name == None:
        inviteName = "【格式问题】不支持爬取名称"
        pass
    else:
        inviteName = name.text
    # print(soup)
    # print(tables)
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
                        break
                a = a + 1
            else:
                if index == -1:
                    range = "列表中未能找到【服务范围】或【施工范围】"
                    break
                else:
                    range = tds[index].find(text=True)
                pass

    for bidder in bidders:
        # price_text = []
        # supplier_text = []
        # 价格下标
        price_index = 0
        # 供应商下标
        supplier_index = 0
        ths = bidder.findAll("th")
        trs = bidder.findAll("tr")
        # 获取对应值的下标
        for i, th in enumerate(ths):
            th_value = th.find(text=True)
            if th_value == "中标（成交）金额(元)":
                price_index = i
                continue
            elif th_value == "中标供应商名称":
                supplier_index = i
                continue

        for td in trs:
            price = td.find("td", {"class": "code-summaryPrice"})
            supplier = td.find("td", {"class": "code-winningSupplierName"})
            if price == None:
                continue
            else:
                price_text = price.text.strip()
                supplier_text = supplier.text.strip()
                if price_text == '':
                    price_text = '第三种情况'
                continue

    # 项目名称
    projectName = reqdata['result']['data']['projectName']
    # 发布时间
    publishDate = reqdata['result']['data']['publishDate']
    time_local = time.localtime(int(publishDate / 1000))
    dt = time.strftime("%Y-%m-%d", time_local)
    webUrl = Url_web + '?articleId=' + articleId
    alldata = {"inviteName": inviteName, "projectName": projectName, "range": range, "dt": dt, "price_text": price_text,
               "supplier_text": supplier_text, "webUrl": webUrl}
    # alldata = [inviteName,projectName,range,dt,biddersList,webUrl]
    # print(biddersList)
    # print(price_text)
    # print(supplier_text)
    # print(dt)
    # print(projectName)
    # print(range)
    # print(inviteName)
    # print(webUrl)
    return alldata
    pass


# 生成excle
def exportExcle(datas):
    dictionary = {"inviteName":1,"projectName":2,"range":3,"dt":4,"price_text":5,"supplier_text":6,"webUrl":7}

    work_book = xlwt.Workbook(encoding="UTF-8")
    worksheet = work_book.add_sheet("爬取数据")

    # 设置居中样式
    styleCenter = xlwt.XFStyle()  # 创建Style对象
    alignment = xlwt.Alignment()  # 创建Alignment对象
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 设置水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 设置垂直居中
    styleCenter.alignment = alignment  # 将Alignment对象应用到Style对象中

    # 生成表头
    for title in Excel_head:
        worksheet.write(0, title, Excel_head[title], styleCenter)
        pass
    # 循环将值插入表格中
    for i, data in enumerate(datas):
        worksheet.write(i + 1, 0, i + 1, styleCenter)
        #根据字典表中的key与value进行循环遍历数据
        for key, value in dictionary.items():
            worksheet.write(i + 1, value, data[key], styleCenter)

    # 存储excle
    work_book.save("浙江政府采购网中标（成交）结果公告"+str(t)+".xlsx")
    #work_book.save(route + "浙江政府采购网中标（成交）结果公告" + str(t) + ".xlsx")

    pass


def start():
    returnData = []
    articleIds = crawlingCategory(request_head)
    for i in articleIds:
        data = crawlingDetail(i)
        returnData.append(data)
    pass
    # print(returnData)
    exportExcle(returnData)


# 程序停止
def stop():
    pass


# 程序main开始
if __name__ == '__main__':
    start()
    pass
