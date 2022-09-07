import requests
import time
import json
import asyncio
import random
import time
import datetime
import pyppeteer
import os
from git import Repo
import sys
from pyppeteer import launch
import logging
import sqlite3

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename=sys.argv[0]+"baobei.log",     level=logging.INFO, format=FORMAT)


def get_userlist():

    user_list = []

    conn = sqlite3.connect('/home/auto-pdsu-jkbb/jkbb-meta-server/keystone.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM jkbb")
    for row in cursor:
        user_list.append(
            {
                "account": row[1],
                "password": row[2],
                "departName": row[3],
                "instructorName": row[4],
                "address": row[5],
                "latitude": row[6],
                "longitude": row[7],
                "permanentAddress": row[8],
                "isStayLocal": row[9],
                "isStaySchool": row[10],
                "phone_number": row[11],
                "emergencyName": row[12],
                "emergencyPhone": row[13],
                "token": "",
            }
        )
    conn.close()
    return user_list


def push_log_git():
    dirfile = os.path.abspath('/home/auto-pdsu-jkbb/')
    repo = Repo(dirfile)
    # 上传log到git仓库
    g = repo.git
    g.add("--all")
    g.commit("-m update: auto push log")
    g.push()
    print("Successful push!")

def push_resp(user):
    '''

    请求健康报备

    以下参数均为健康报备的录入信息，请在上面的个人信息字典修改
    departName: 学生班级
    instructorName: 辅导员名字
    nucleicAcidDate: 核酸时间
    address: 当前位置
    latitude: 当前位置的经度(保留4位小数)
    longitude: 当前位置的纬度(保留6位小数)
    permanentAddress: 本人常住地址
    isStayLocal: 是否在平顶山 0不在1在
    isStaySchool: 是否在校 0不在1在
    phone_number: 手机号
    emergencyName: 紧急联系人姓名
    emergencyPhone: 紧急联系人手机号
    token: 用于登陆的token（每天需要获取新的）

    '''

    try_num = 0
    # 最多重试5次
    while try_num < 5:
        try:
            payload = {
                "backPdsDate": None,
                "backSchoolDate": None,
                "leaveSchoolDate": None,
                "onceIllDate": None,
                "recoveryDate": None,
                "touchDate": None,
                "unusualIllDate": None,
                "nucleicAcidDate": (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),
                "needUpdate": 1,
                "isAgree": True,
                "createTime": time.strftime("%Y-%m-%d %H:%M:%S"),
                "age": "21",
                "phone": user["phone_number"],
                "dormitory": None,
                "departName": user["departName"],
                "address": user["address"],
                "latitude": user["latitude"],
                "longitude": user["longitude"],
                "permanentAddress": user["permanentAddress"],
                "emergencyName": user["emergencyName"],
                "instructorName": user["instructorName"],
                "emergencyPhone": user["emergencyPhone"],
                "healthCodeStatus": 1,
                "yellowHealthCode": None,
                "redHealthCode": None,
                "backHealthCodeStatus": None,
                "strokeCodeStatus": 1,
                "yellowStrokeCode": None,
                "isCommunityHasAddress": None,
                "redStrokeCode": None,
                "contactType": None,
                "isStayLocal": user["isStayLocal"],
                "isStaySchool": user["isStaySchool"],
                "outType": 2,
                "isInternship": 0,
                "bodyTemperature": 36.5,
                "unusualSymptom": None,
                "backSchoolSymptom": None,
                "leaveSchoolSymptom": None,
                "isTouchIll": None,
                "nucleicResult": 0,
                "otherSymptomRemark": None,
                "backSchoolOtherSymptom": None,
                "leaveSchoolOtherSymptom": None,
                "touchIllAddress": None,
                "touchIllDetail": None,
                "treatDetail": None,
                "villageAddress": None,
                "homieConfirmTime": None,
                "reachRiskAreaTime": None,
                "homieAddress": None,
                "isColdChain": None,
                "homieTouchIll": None,
                "vehicleType": None,
                "leavePdsAddress": None,
                "goRiskAddress": None,
                "backDetailAdress": None,
                "backBeforeDetailAdress": None,
                "backSchoolBeforeDetailAdress": None,
                "leaveSchoolGoDetailAdress": None,
                "isOverseas": None,
                "isCommunityHas": None,
                "hospitalDetail": None,
                "onceTreatHospital": None,
                "isolationType": None,
                "backIsolationType": None,
                "backSchoolIsolationType": None,
                "leaveSchoolIsolationType": None,
                "isolateStartTime": None,
                "isolateEndTime": None,
                "isolateReasons": None,
                "isolatePlace": None,
                "todayIsArea": "1",
                "backSchoolTodayIsArea": None,
                "leaveSchoolTodayIsArea": None,
                "backNucleicAcidResult": None,
                "backSchoolNucleicAcidResult": None,
                "leaveSchoolNucleicAcidResult": None,
                "remark": None,
                "backSchoolRemark": None,
                "leaveSchoolRemark": None
            }
            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Dest': 'document',
                'content-type': 'application/json;charset=UTF-8',
                'X-Device-Info': 'APP',
                'X-Terminal-Info': 'APP',
                'Referer': 'https://yqfk.pdsu.edu.cn/serv-h5/?token='+user["token"],
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cookie': 'Domain=.pdsu.edu.cH; Path=/',
                'X-Id-Token': user["token"]
            }
            url = "https://yqfk.pdsu.edu.cn/smart-boot/api/healthReport/saveHealthReport"

            response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False, timeout=15)

        except Exception as e:
            print(e)
            try_num += 1
        else:
            logging.info(response.text)
            return
        logging.info(user["phone_number"]+" "+"push_resp 请求超时")


async def get_token(account, password):

    '''

    获取token

    account: “i平院”app登陆账号（手机号、学号）
    password: “i平院”app登陆密码

    '''

    try_num = 0
    # 最多重试5次
    while try_num < 5:
        try:
            # 启动浏览器
            # browser = await launch(options={'args': ['--no-sandbox']})
            browser = await launch()
            page = await browser.newPage()

            # 进入登陆页
            await page.goto('https://superapp.pdsu.edu.cn')
            await asyncio.sleep(10)

            # 输入账号密码，并点击登陆
            await page.type('#username', account)
            await page.type('#password', password)
            await page.click('#fm1 > div:nth-child(5) > div > input.el-button.el-button--primary.el-button--medium.is-round')

            # 从cookie中提取token
            await asyncio.sleep(5)
            cookies = await page.cookies()
            user_cookie = cookies[0]["value"]

            # 关闭浏览器
            await browser.close()

        except Exception as e:
            print(e)
            # 出现异常，关闭浏览器重试
            logging.info(account+" "+password+" 获取token失败")
            await browser.close()
            try_num += 1
            push_log_git()
        else:
            # 成功即返回token
            logging.info(account+" "+password+" 获取token成功")
            print(account+" "+password+" 获取token成功")
            push_log_git()
            return user_cookie

if __name__ == '__main__':
    user_list = get_userlist()
    print(user_list)
    for user in user_list:
        #time.sleep(random.randint(1, 500))
        # 获取token
        user_token = asyncio.get_event_loop().run_until_complete(get_token(user["account"], user["password"]))
        user["token"] = user_token

        # 请求健康报备
        push_resp(user)
        logging.info("------------------------------")
