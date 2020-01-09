# _*_coding:utf-8_*_
from __future__ import unicode_literals

from argoagent  import *
import threading
from multiprocessing import Process
import time
'''
server_url为数据上传的地址

python_sdk_platform为数据来源平台。如:服务端收到从Android平台传来的数据后，若使用python SDK采集数据,此时platform字段填写Android,便于数据归类统计分析。
建议传入字段如：iOS/Android/JS/WeChat.（不区分大小写）。限传字符串类型。demo中假定该后台数据对应移动端Android数据。

python SDK使用场景示例如下：
'''
server_url = "https://XXX:4089"
python_sdk_platform = "js"
appkey = "fangzhouargo"
log_path = "XXX"
class Demo():
    def pythonsdkdemo(self):

        # 默认方式发送数据，数据逐条发送
        # collector = DefaultCollecter(server_url)
        # 批量发送数据，数据达到一定条数或达到相应时间进行批量发送
        # collector = BatchCollecter(server_url, 10, 2, 100, 1000, request_timeout=None)
        collector = LogCollecter(log_path,is_batch=True,batch_num=10,general_rule="hour")

        eguan = AnalysysPythonSdk(collector)


        # 注意：此方法为必须调用方法。设置项目名称，用户请填写在数据端新建的项目appkey，例如：
        eguan.setAppId(appkey)

        #设备debug模式，允许设置0,1,2.默认为0,不打印日志，数据进行统计分析。设置为1时打印日志，上传的数据不进行统计分析。设置为2时打印日志，上传的数据进行统计分析。例如：
        eguan.setDebugMode(1)

        #设置匿名ID，此ID为用户未登陆状态下使用的数据上传用户ID。此ID可以由用户自己定义，如果移动端接入Android SDK，此ID也可以从Android SDK端获取传到后台。
        distinct_id = "ABCD123456"
        '''
        假定用户场景： 用户先将未登陆状态下的数据传到方舟后台进行统计。当发生登陆行为后，以登录的用户ID向方舟后台发送数据。
        说明：
        1、未登录状态下发送的数据，is_login参数必须设置为False
        2、在集成SDK时，在登录位置需调用alias接口。在数据逻辑上形成登录状态，之后在方舟上可以看到该登录ID用户与之前匿名ID用户的数据为同一用户。
        3、登录后发送数据，is_login参数必须设置为True
        4、登录后发送数据，形参distinct ID应使用已登录的ID，而非匿名ID。
        
        '''
        #记录普通用户浏览商品详情，商品的属性随事件上传（用户未登录）
        commodity_properties = {
            "commodity_name" : "跑步机",
            "commodity_brand" : "zhonghua",
            "commodity_price" : 5000,
            "commodity_quality" : True,
            "commodity_function" : ["run","记录心率"]
        }


        for i in range(100):
            eguan.track(distinct_id,"SearchCommodity",commodity_properties,python_sdk_platform,is_login=False)

        # 记录普通用户点击注册按钮，注册事件未携带属性（用户未登录）
        eguan.track(distinct_id,"register",None,python_sdk_platform,is_login=False)

        #用户进行登录。假定alias_id为用户登录后的ID
        alias_id = "zhangsan"
        eguan.alias(alias_id,distinct_id,python_sdk_platform)

        #用户登录后，需要将该用户的用户属性上传
        profile_properties = {
            "sex" : "男",
            "phonenumber" : "13966667777",
            "email" : "xxx@163.com",
            "hobby" : ["basketball","听音乐","mountain-climbing"],
            "is_female" : False
        }
        eguan.profile_set(alias_id,profile_properties,python_sdk_platform,is_login=True)

        # 用户登录，且上传用户属性后，继续浏览APP，再之后用户进行购买、支付等操作。用户在购买、支付等行为追踪时，想带上该商品的属性。
        # 注册通用属性（当通用属性设置后，之后的事件均携带该通用属性）
        super_properties = {
            "commodity_name" : "减肥药",
            "commodity_brand" : "luomiou",
            "commodity_price" : 1000,
            "commodity_quality" : True,
        }

        eguan.registerSuperProperties(super_properties)

        #获取已存在的通用属性
        # eguan.getAllSuperProperties()
        #获取单个通用属性
        # eguan.getSingleSuperProperties("commodity_name")

        #记录购买button被点击
        purchase_properties = {
            "Referer" : "gouwuche"
        }

        eguan.track(alias_id,"purchase",purchase_properties,python_sdk_platform,is_login=True)

        #记录支付行为
        payment_properties = {
            "pay_usage" : "Wechat"
        }
        eguan.track(alias_id,"payment",payment_properties,python_sdk_platform,is_login=True)
        #批量发送时，将队列中缓存的数据立即上传
        eguan.close()



if __name__ == '__main__':

    EG = Demo()
    P1=Process(target=EG.pythonsdkdemo())
    P2 = Process(target=EG.pythonsdkdemo())
    P1.start()
    P2.start()
    # EG.pythonsdkdemo()