# _*_coding:utf-8_*_

import gzip
import base64
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

class AnalysysPythonSdkNetworkException(Exception):

    '''
    在因为网络或其他异常导致数据发送失败时，AnalysysPythonSdk会抛出此异常，用户应该捕获并处理
    '''
    pass

class DefaultCollecter(object):

    def __init__(self,server_url,request_timeout=None):
        self._server_url = server_url+"/up"
        self._request_timeout = request_timeout
        self._response = 0

    @staticmethod
    def _gzipCompressData(data):
        try:
            return gzip.compress(data)
        except AttributeError:
            from cStringIO import StringIO
            buffer = StringIO()
            f = gzip.GzipFile(mode="wb",fileobj=buffer)
            try:
                f.write(data)
            finally:
                f.close()
            return buffer.getvalue()

    def _sendRequest(self,data):
        try:
            request = urllib2.Request(self._server_url,data)
            if self._request_timeout is not None:
                response = urllib2.urlopen(request, timeout=self._request_timeout)
                self._response = response.getcode()
            else:
                response = urllib2.urlopen(request)
                self._response = response.getcode()
        except urllib2.HTTPError as e:
            raise AnalysysPythonSdkNetworkException("The server could't fulfill the request. Error code:",e)
        except urllib2.URLError as e:
            raise AnalysysPythonSdkNetworkException("Failed to reache the server. Reason:",e)
        return True

    def _base64Data(self,data):
        return  base64.b64encode(self._gzipCompressData(data.encode("utf-8")))

    def uploadData(self,data):
        original_data = []
        original_data.append(data)
        if data["xcontext"]["$debug"] == 1 or data["xcontext"]["$debug"] == 2:
            print("Send message to server:",self._server_url,"data(Defaultcollecter):",original_data)
        original_data = json.dumps(original_data,ensure_ascii=False)
        return self._sendRequest(self._base64Data(original_data))

    def flush(self):
        pass

    def close(self):
        pass