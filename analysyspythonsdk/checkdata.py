# _*_coding:utf-8_*

import re
try:
    isinstance("",basestring)
    def is_str(s):
        return isinstance(s,basestring)
except NameError:
    def is_str(s):
        return isinstance(s,str)

class AnalysysPythonSdkIllegalDataException(Exception):
    '''
    在发送的数据格式不符合规范时，AnalysysPythonSdk会抛出此异常，用户应该捕获并处理
    '''
    pass

def checkData(data):
    key_pattern = re.compile(r"(^xwhat$|^xwhen$|^xwho$|^appid$|^xcontext$|^$lib$|^$is_login$|^$lib_version$|^$debug$)", re.I)
    key_pattern_regular = re.compile(r"^[a-zA-Z$][a-zA-Z0-9_$]{0,99}$", re.I)
    for key, value in data.items():
        if not key_pattern.match(key):
            raise AnalysysPythonSdkIllegalDataException("xhwat、xwho、xhen、appid、xcontext、$lib、$lib_version、$is_login、$debug are AnalysysPythonSdk reserved words.")

        if key == "appid":
            if not is_str(value):
                raise AnalysysPythonSdkIllegalDataException("The input appid must be string.")
            if value is None or len(str(value))==0:
                raise AnalysysPythonSdkIllegalDataException("The input appid can not be empty")
            if len(str(value)) > 255:
                raise AnalysysPythonSdkIllegalDataException("The max lenth of the input appid is 255.")

        if key == "xwho":
            if not is_str(value):
                raise AnalysysPythonSdkIllegalDataException("The input distinct_id must be string.")
            if value is None or len(str(value))==0:
                raise AnalysysPythonSdkIllegalDataException("The input distinct_id can not be empty.")
            if len(str(value)) > 255:
                raise AnalysysPythonSdkIllegalDataException("The max lenth of the input distinct_id is 255.")

        if key == "xwhat":
            if not is_str(value):
                raise AnalysysPythonSdkIllegalDataException("The input event_name must be string.")
            if value is None or len(str(value))==0:
                raise AnalysysPythonSdkIllegalDataException("The input event_name can not be empty.")
            if not key_pattern_regular.match(value):
                print(value,"The imput eventName must be begin with $ or a-zA-Z,and contains $ a-z A-Z 0-9 _")

        if isinstance(value,dict):
            if len(value) > 300:
                raise AnalysysPythonSdkIllegalDataException("The max count of properties is 300")
            for xcontext_key,xcontext_value in value.items():
                if xcontext_key is None or len(str(xcontext_key)) == 0:
                    print("Warning:key empty.")
                else:
                    if xcontext_key == "$original_id":
                        if not is_str(xcontext_value):
                            raise AnalysysPythonSdkIllegalDataException("The input original_id must be string.")
                        if xcontext_value is None or len(str(xcontext_value)) == 0:
                            raise AnalysysPythonSdkIllegalDataException("The input original_id can not be empty.")
                        if len(str(xcontext_value)) > 255:
                            raise AnalysysPythonSdkIllegalDataException("The max length of the input original_id is 255.")
                    if not is_str(xcontext_key):
                        raise AnalysysPythonSdkIllegalDataException("The input xcontext key must be string.")
                    if key_pattern.match(xcontext_key):
                        raise AnalysysPythonSdkIllegalDataException("xhwat、xwho、xhen、appid、xcontext、$lib、$lib_version、$is_login、$debug are AnalysysPythonSdk reserved words.")
                    if not key_pattern_regular.match(xcontext_key):
                        print("Warning:The input key must be begin with $ or a-zA-Z,and contains $ a-z A-Z 0-9 _")
                    if is_str(xcontext_value):
                        if data["xwhat"] != "$profile_unset":
                            if xcontext_value is None or len(str(xcontext_value)) == 0:
                                print("Warning:Value empty.")
                        if len(str(xcontext_value)) > 255:
                            print("Warning:The max length of string are 255")
                        if len(str(xcontext_value)) > 8192:
                            value[xcontext_key] = xcontext_value[0:8192] + "$"
                    # 若代码中用到了元组，请先转为List
                    if isinstance(xcontext_value, list):
                        for list_key in xcontext_value:
                            if list_key is None or len(str(list_key)) == 0:
                                print("Warning:Value empty.")
                            if not is_str(list_key):
                                raise AnalysysPythonSdkIllegalDataException("The input list value must be string.")
                            if len(str(list_key)) > 255:
                                print("Warning:The max length of string is 255")
                            if len(str(list_key)) > 8192:
                                xcontext_value.remove(list_key)
                                xcontext_value.append(list_key[0:8192]+"$")
                        if len(xcontext_value) > 100:
                            raise AnalysysPythonSdkIllegalDataException("The max length of list are 100.")

    return data