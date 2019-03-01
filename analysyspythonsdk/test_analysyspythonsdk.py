# _*_coding:utf-8_*_
from __future__ import unicode_literals

from argoagent  import *
'''
server_url为数据上传的地址

python_sdk_platform为数据来源平台。如:服务端收到从Android平台传来的数据后，若使用python语言版SDK采集数据,此时platform字段填写Android,便于数据统计分析。
建议传入字段如：iOS/Android/JS/WeChat.（不区分大小写）。限传字符串类型。

python SDK使用场景示例如下：
'''
# 场景一：实时发送方式，初始化python SDK，记录用户登录
server_url = "https://sdk.analysys.cn:4089"
python_sdk_platform = "android"
class Demo():
    def testDefaultCollecter(self):
        collector = DefaultCollecter(server_url)
        eguan = AnalysysPythonSdk(collector)
        #注意：此方法为必须调用方法。设置项目名称，用户请填写在数据端新建的项目名，例如：
        eguan.setAppId("ssss")
        #设备debug模式，允许设置0,1,2.默认为0,不打印日志，数据进行统计分析。设置为1时打印日志，上传的数据不进行统计分析。设置为2时打印日志，上传的数据进行统计分析。例如：
        eguan.setDebugMode(2)
        #记录用户登录事件
        distinct_id = "aaaaa"
        eguan.track(distinct_id,"u7777777",None,python_sdk_platform,is_login=True,)
        # eguan.close()

        #场景二：某电商追踪用户浏览商品和下订单等事件
        superProperties = {
            "member" : "VIP",
            "age" : 20

        }
        eguan.registerSuperProperties(superProperties)
        eguan.getAllSuperProperties()
        eguan.getSingleSuperProperties("member")
        distinct_id = "ABCDE112345"
        properties = {
            #浏览商品用户的外网IP
            "ip" : "169.169.169.169",
            #浏览商品的时间
            "view_time" : time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
            #浏览商品的ID
            "productId" : "666",
            #浏览商品的类别
            "productCatalog" : "electronic",
            "$debug" : "android",
            "$lib" : "AAAAAAA",
             "abc" : ""
        }
        #浏览商品跟踪

        eguan.track(distinct_id,"view_product",properties,python_sdk_platform,False)
        eguan.unregisterSuperProperties("age")
        eguan.getAllSuperProperties()

        properties = {
            "productList" : ["iphone X","honor P8","computer"],
            "productPrice" : 23456,
            "isPay" : True
        }
        #商品是否支付跟踪
        eguan.track(distinct_id,"payment",properties,python_sdk_platform,True)
        eguan.close()

        #场景三：用户识别
        alias_id = "12345"
        distinct_id = "xiaoming"
        #调用alias方法，将用户登录前和登录后的ID进行关联
        eguan.alias(alias_id,distinct_id,python_sdk_platform)

        #场景四：设置用户属性
        distinct_id = "CCCCCCCCCCCCC"
        properties = {
            "name": "梅西",
            "sex": "male",
            "age": 31,
            "login_time": time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
            "$email" : "XXX@qq.com"
        }
        eguan.profile_set(distinct_id,properties,python_sdk_platform,True)

        #场景五：设置用户只在首次设置时有效的属性
        distinct_id = "DDDDDDDDDDDDD"
        properties = {
            "sex" : "female",
            "activationTime" : "1534249333700"
        }
        eguan.profile_set_once(distinct_id,properties,python_sdk_platform)

        #场景六：设置用户数值型属性
        distinct_id = "EEEEEEEEEEEEE"
        eguan.profile_increment(distinct_id,{"gameAge":2},python_sdk_platform)

        #场景七：设置用户列表类型属性
        distinct_id = "FFFFFFFFFFFF"
        properties = {
            "hobby" : ["basketball","music","read"],
            "movies" : ["大话西游","一出好戏"]
        }
        eguan.profile_append(distinct_id,properties,python_sdk_platform,True)

        #场景八：删除用户属性
        distinct_id = "HHHHHHHHHHH"
        eguan.profile_unset(distinct_id,["hobb"],python_sdk_platform,True)

        #场景九：清除所有用户属性
        distinct_id = "GGGGGGGGGG"
        eguan.profile_delete(distinct_id,python_sdk_platform,True)

    def testBatchCollecter(self):
        collector = BatchCollecter(server_url, 20, 3, 100, 1000, request_timeout=None)
        analysys = AnalysysPythonSdk(collector)
        analysys.setDebugMode(2)
        analysys.setAppId("Eguan")
        analysys.registerSuperProperties({"sex": "male", "name": "普京", "age": 50})
        for i in range(10):
            analysys.track("s12345678", "$xwhat", None,python_sdk_platform, True)
        analysys.unregisterSuperProperties("age")
        property = {
                    "ip": "10.20.30.40",
                    "name": "勒布朗詹姆斯",
                    "sex": "male",
                    "salary": 4000,
                    "hobby": ["basketball", "book", "听音乐"],
                    "isSuperStar": True,
                    "birthTime":"1984-12-30 13:13:13"

                }
        analysys.registerSuperProperties({"sex": "female", "location": "beijing"})
        analysys.track("a1234567890", "track_event", property, python_sdk_platform,True)
        analysys.alias("xiaoming", "zhangsan",python_sdk_platform)
        analysys.profile_set("555", property,python_sdk_platform)
        analysys.profile_set_once("666", {"registerTime": "2018-08-05"},python_sdk_platform)
        analysys.profile_increment("777", {"age": 20},python_sdk_platform)
        analysys.profile_append("123321", {"property": [1, "中文"]},python_sdk_platform)
        analysys.profile_unset("123321", ["interest"], python_sdk_platform,True)
        analysys.profile_delete("123321",python_sdk_platform)
        analysys.close()

if __name__ == '__main__':
    EG = Demo()
    EG.testDefaultCollecter()
    time.sleep(2)
    EG.testBatchCollecter()