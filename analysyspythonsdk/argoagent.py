# _*_coding:utf-8_*_

from __future__ import unicode_literals
import time
import platform
import re
from analysyspythonsdk.checkdata import checkData
from analysyspythonsdk.defaultcollecter import *
from analysyspythonsdk.batchcollecter import *

# print(platform.python_version())
__PYTHON_SDK_VERSION__ = "4.0.6"
if re.match(r"^2",platform.python_version()):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

class AnalysysPythonSdk(object):

    def __init__(self,collector=None):
        self._collector = collector
        self._super_properties = {}
        self.debug_mode = 0
        self.appid = "analysys"

    @staticmethod
    def _current_time():
        return int(time.time() * 1000)

    '''
    debug_mode为是否需要调试模式，默认值为0，不输出任何日志，数据端对debug_mode为0的上传数据进行统计分析。支持设置为1或为2。设置为1时，输出相应的日志，
    但数据端不会对debug_mode为1的数据进行统计分析。设置为2时，输出相应的日志，数据端对debug_mode为2的数据进行统计分析。
    '''
    def setDebugMode(self,debug_mode=0):
        if  debug_mode == 1 or debug_mode == 2:
            self.debug_mode = debug_mode
        else:
            self.debug_mode = 0

    '''
     appid为项目名称，用户请填写在数据端新建的项目名. 若与数据端新建不同，将导致上传数据无法正常入库.默认值为analysys
    '''
    def setAppId(self,appid):
        self.appid = appid

    def registerSuperProperties(self,super_properties):
        '''
        设置每个事件都带有的公共属性，当track中的properties和registerSuperProperties有相同的key值时，track中的将覆盖后者
        :param super_properties:公共属性，传入参数为dict类型
        '''
        self._super_properties.update(super_properties)

    def unregisterSuperProperties(self,super_properties_key):
        '''
        删除某个已设置的事件公共属性
        :param super_properties_key: 所需删除属性的key，传入参数为string类型
        '''
        if super_properties_key in self._super_properties.keys():
            self._super_properties.pop(super_properties_key)

    def getSingleSuperProperties(self,super_properties_key):
        '''
        获取已设置的事件公共属性
        :param super_properties_key:所需获取属性的key， 传入参数为string类型
        :return: 事件公共属性对应的value
        '''
        if super_properties_key in self._super_properties.keys():
            print(self._super_properties[super_properties_key])

    def getAllSuperProperties(self):
        '''
        获取已设置的所有事件公共属性
        '''
        if self._super_properties is not None:
            print(self._super_properties)

    def clearSuperProperties(self):
        '''
        清除所有已设置的事件公共属性
        '''
        self._super_properties = {}

    def track(self,distinct_id,event_name,event_properties,data_platform,is_login=False):
        '''

        :param distinct_id: 用户唯一标识
        :param event_name: 事件名称
        :param event_properties: 事件自带属性,dict类型
        :param data_platform: 数据来源平台
        :param is_login:是否为登录用户
        '''
        event_all_properties = self._super_properties.copy()
        if event_properties:
            event_all_properties.update(event_properties)
        self._dataStructure("track",event_name,distinct_id,None,event_all_properties,data_platform,is_login)


    def alias(self,alias_id,distinct_id,data_platform,alias_properties=None):
        '''
        在distinctId发生变化的时候调用，用来通知SDK distinctId变化前后的ID对应关系.如注册时，注册前的distinctId和注册后的distinctId关联
        :param alias_id: 注册后的用户唯一标识
        :param distinct_id: 注册前的用户唯一标识
        :param data_platform: 数据来源平台
        :param alias_properties: 事件属性，dict类型
        '''
        alias_all_properties = {}
        if alias_properties:
            alias_all_properties.update(alias_properties)
        self._dataStructure("alias",None,alias_id,distinct_id,alias_all_properties,data_platform,is_login=False)

    def profile_set(self,distinct_id,profile_properties,data_platform,is_login=False):
        '''
        设置一个用户的profile，如果已存在则覆盖
        :param distinct_id: 用户唯一标识
        :param profile_properties: 用户属性，传入dict类型
        :param data_platform: 数据来源平台
        :param is_login: 是否为登录用户
        '''
        if profile_properties:
            return self._dataStructure("profile_set",None,distinct_id,None,profile_properties,data_platform,is_login)

    def profile_set_once(self,distinct_id,profile_properties,data_platform,is_login=False):
        '''
        设置一个用户的profile，如果某个profile存在则不设置
        :param distinct_id: 用户唯一标识
        :param profile_properties: 用户属性，dict类型
        :param data_platform: 数据来源平台
        :param is_login: 是否为登录用户
        '''
        if profile_properties:
            return self._dataStructure("profile_set_once",None,distinct_id,None,profile_properties,data_platform,is_login)

    def profile_increment(self,distinct_id,profile_properties,data_platform,is_login=False):
        '''
        增加/减少一个用户的某一个或多个数值类型的profile
        :param distinct_id: 用户唯一标识
        :param profile_properties: 用户属性，dict类型，value为数值类型
        :param data_platform: 数据来源平台
        :param is_login: 是否为登录用户
        '''
        if profile_properties:
            return self._dataStructure("profile_increment",None,distinct_id,None,profile_properties,data_platform,is_login)

    def profile_append(self,distinct_id,profile_properties,data_platform,is_login=False):
        '''
          追加一个用户的某一个或多个集合类型的profile
        :param distinct_id: 用户唯一标识
        :param profile_properties: 用户属性，dict类型，value为list类型
        :param data_platform: 数据来源平台
        :param is_login:是否为登录用户
        '''
        if profile_properties:
            return self._dataStructure("profile_append",None,distinct_id,None,profile_properties,data_platform,is_login)

    def profile_unset(self,distinct_id,profile_properties_keys,data_platform,is_login=False):
        '''
        删除一个用户的某一个或多个profile已上传属性
        :param distinct_id: 用户唯一标识
        :param profile_properties_keys: 用户所需删除profile的key，传入list类型。如：["abc"]
        :param data_platform: 数据来源平台
        :param is_login: 是否为登录用户
        '''
        if profile_properties_keys:
            if not isinstance(profile_properties_keys,list):
                print("The input keys must list.")
            return self._dataStructure("profile_unset",None,distinct_id,None,profile_properties_keys,data_platform,is_login)

    def profile_delete(self,distinct_id,data_platform,is_login=False):
        '''
         删除用户所有信息
        :param distinct_id: 用户唯一标识
        :param data_platform: 数据来源平台
        :param is_login: 是否为登录用户
        '''
        return self._dataStructure("profile_delete",None,distinct_id,None,{},data_platform,is_login)

    def _dataStructure(self,event_type,event_name,distinct_id,original_id,properties,data_platform,is_login):
        data = {
            "appid": self.appid,
            "xwho": distinct_id,
            "xwhat": event_name,
            "xwhen":self._current_time(),
            "xcontext": properties
        }
        lib_properties = {
            "$lib": "python",
            "$lib_version": __PYTHON_SDK_VERSION__,
            "$is_login": False,
            "$debug": self.debug_mode,
            "$platform": None
        }
        if event_type == "track" :
            properties.update(lib_properties)
            data["xwhat"] = event_name
        if event_type in ["alias","profile_set","profile_set_once","profile_increment","profile_append","profile_delete"] :
            properties.update(lib_properties)
            data["xwhat"] = "$" + event_type
        if event_type == "alias" :
            data["xcontext"]["$original_id"] = original_id
            data["xcontext"]["$is_login"] = True
        if event_type == "profile_unset":
            data["xwhat"] = "$profile_unset"
            data["xcontext"] = lib_properties
            for key in properties:
                d_properties = {key : ""}
                data["xcontext"].update(d_properties)
        if is_login:
            data["xcontext"]["$is_login"] = True
        if data_platform:
            if data_platform.lower() == "ios" :
                data["xcontext"]["$platform"] = "iOS"
            elif data_platform.lower() == "android" :
                data["xcontext"]["$platform"] = "Android"
            elif data_platform.lower() == "js" :
                data["xcontext"]["$platform"] = "JS"
            elif data_platform.lower() == "wechat":
                data["xcontext"]["$platform"] = "WeChat"
            else:
                if self.debug_mode == 1 or self.debug_mode == 2 :
                    print("Warning:param platform: %s" %(data_platform) + " Your input are not:iOS/Android/JS/WeChat.")
                data ["xcontext"]["$platform"] = data_platform
        data = checkData(data)
        self._collector.uploadData(data)
        time.sleep(0.2)

    def flush(self):
        self._collector.flush()

    def close(self):
        self._collector.close()
