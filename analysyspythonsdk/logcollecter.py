# _*_coding:utf-8_*_

import time
import json
import codecs
import os
try:
    import queue as Queue
except ImportError:
    import Queue

class AnalysysPythonSdkFileException(Exception):

    '''
    在因为文件目录不存在时，AnalysysPythonSdk会抛出此异常，用户应该捕获并处理
    '''
    pass


if os.name == "posix":
    import fcntl
    def lockFile(f):
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
        except IOError as e:
            raise AnalysysPythonSdkFileException

    def unLockFile(f):
        fcntl.flock(f,fcntl.LOCK_UN)
elif os.name == "nt":
    import msvcrt
    def lockFile(f):
        try:
            fp_position = f.tell()
            f.seek(0)
            try:
                msvcrt.locking(f.fileno(),msvcrt.LK_LOCK,1)
            except IOError as e:
                raise AnalysysPythonSdkFileException(e)
            finally:
                if fp_position:
                    f.seek(fp_position)
        except IOError as e:
            raise AnalysysPythonSdkFileException(e)

    def unLockFile(f):
        try:
            fp_position = f.tell()
            if fp_position:
                f.seek(0)
            try:
                msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
            except IOError as e:
                raise AnalysysPythonSdkFileException(e)
            finally:
                if fp_position:
                    f.seek(fp_position)
        except IOError as e:
            raise AnalysysPythonSdkFileException(e)
else:
    raise AnalysysPythonSdkFileException("This system is not applicable.")

class LogCollecter(object):

    def __init__(self,log_path,is_batch=False,batch_num=20,general_rule="hour"):
        self._log_path = log_path
        self._is_batch = is_batch
        self._batch_num = batch_num
        self._general_rule = general_rule
        self._queue = Queue.Queue()
        self._queue.put(1)
        self.filename = None
        self._original_data = []

    def _logPath(self):
        if not os.path.exists(self._log_path):
            raise AnalysysPythonSdkFileException("Please check whether the file directory exists！")
        if self._general_rule.lower() == "day":
            self.filename = self._log_path + "/" + "datas_" + time.strftime("%Y%m%d",time.localtime()) + ".log"
        else:
            self.filename = self._log_path + "/" + "datas_" + time.strftime("%Y%m%d%H",time.localtime()) + ".log"
        return self.filename

    def _writeData(self,data):

        try:
            with open(self._logPath(), "a", encoding="utf-8") as f:
                lockFile(f)
                if isinstance(data, dict):
                    f.write(json.dumps(data, ensure_ascii=False))
                if isinstance(data, str):
                    f.write(data)
                f.write("\n")
                unLockFile(f)
        except TypeError:
            with codecs.open(self._logPath(),"a",encoding="utf-8") as f:
                lockFile(f)
                if isinstance(data, dict):
                    f.write(json.dumps(data, ensure_ascii=False))
                if isinstance(data, str):
                    f.write(data)
                f.write("\n")
                unLockFile(f)

    def _queueData(self,data):
        msg = None
        self._queue.get(block=True,timeout=None)
        self._original_data.append(json.dumps(data,ensure_ascii=False))
        if len(self._original_data) >= self._batch_num :
            msg = self._original_data
            self._original_data = []
        self._queue.put(1)
        if msg:
            msg = "\n".join(str(i) for i in msg)
            self._writeData(msg)

    def uploadData(self,data):
        if self._is_batch:
            self._queueData(data)
        else:
            self._writeData(data)

    def flush(self):
        msg = None
        self._queue.get(block=True,timeout=None)
        if len(self._original_data) > 0:
            msg = self._original_data
            self._original_data = []
        self._queue.put(1)
        if msg:
            msg = "\n".join(str(i) for i in msg)
            self._writeData(msg)

    def close(self):
        self.flush()










