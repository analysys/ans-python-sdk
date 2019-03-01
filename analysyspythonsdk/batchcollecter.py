# _*_coding:utf-8_*_

import json
from analysyspythonsdk.defaultcollecter import *
from threading import Thread,Event

try:
    import queue as Queue
except ImportError:
    import Queue
class AnalysysPythonSdkNetworkException(Exception):

    '''
    在因为网络或其他异常导致数据发送失败时，AnalysysPythonSdk会抛出此异常，用户应该捕获并处理
    '''
    pass
class BatchCollecter(DefaultCollecter):

    class UploadMonitorThread(Thread):

        def __init__(self, collecter):
            super(BatchCollecter.UploadMonitorThread, self).__init__()
            self._collecter = collecter
            self._stop_event = Event()
            self._finished_event = Event()

        def stop(self):
            # 退出时调用，以保证线程安全结束
            self._stop_event.set()
            self._finished_event.wait()

        def run(self):
            while True:
                self._collecter.need_send.wait(self._collecter.max_interval_time)
                if self._collecter.send():
                    self._collecter.need_send.clear()
                if self._stop_event.isSet():
                    break
            self._finished_event.set()

    def __init__(self,server_url,max_interval_time=15,queue_cache_max_size=10,collecter_max_size=100,queue_max_size=1000,request_timeout=None):
        '''
        初始化 BatchCollecter
        :param server_url: 发送的服务端地址
        :param max_interval_time: 前后发送的间隔时间，单位秒
        :param queue_cache_max_size: 队列缓存的最大值，超过此值将立即发送
        :param collecter_max_size: 单个请求发送的最大值
        :param queue_max_size: 整个队列缓存的最大值
        :param request_timeout: 请求的超时时间，单位毫秒
        '''
        super(BatchCollecter,self).__init__(server_url,request_timeout)
        self._cache_max_size = queue_cache_max_size
        self._collecter_max_size = collecter_max_size
        self.max_interval_time = max_interval_time
        self._queue = Queue.Queue(queue_max_size)

        self.need_send = Event()
        self._original_data = []

        self._monitor_thread= BatchCollecter.UploadMonitorThread(self)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def uploadData(self,data):
        try:
            self._queue.put_nowait(data)
            if data["xwhat"] == "$alias":
                self._original_data.append(data)
                self.flush()
                self._original_data.pop()
        except Queue.Full as e:
            raise AnalysysPythonSdkNetworkException("Queue full:",e)
        if self._queue.qsize() >= self._cache_max_size:
            self.flush()

    def flush(self):
        self.need_send.set()

    def send(self,throw_exception=True):
        send_flag = False
        if len(self._original_data) == 0:
            for i in range(self._collecter_max_size):
                if not self._queue.empty():
                    self._original_data.append(self._queue.get_nowait())
                else:
                    break
        if len(self._original_data) > 0:
            if self._original_data[0]['xcontext']['$debug'] == 1 or self._original_data[0]['xcontext']['$debug'] == 2 :
                print("Send message to server:", self._server_url, "data(Batchcollecter):",self._original_data)
            try:
                self._sendRequest(self._base64Data(json.dumps(self._original_data,ensure_ascii=False)))
                send_flag = True
                self._original_data = []
            except AnalysysPythonSdkNetworkException as e:
                if throw_exception:
                    raise e
        return send_flag

    def close(self):
        self._monitor_thread.stop()
        while not self._queue.empty() or not len(self._original_data) == 0:
            self.send(True)