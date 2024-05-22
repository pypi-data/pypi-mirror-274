import time
from threading import Thread

from ryry import ryry_webapi
from ryry import store
from ryry import taskUtils

class TaskThread(Thread):
    params = False
    idx = 0
    call_back = None
    def __init__(self, idx, func, func_id, params, callback):
        super().__init__()
        self.idx = idx
        self.func = func
        self.widgetid = func_id
        self.params = params
        self.call_back = callback
        if self.call_back == None:
            raise Exception("need callback function")
        self.start()
    def run(self):
        self.checking = False
        self.result = False, "Unknow"
        if self.widgetid == None:
            self.widgetid = ryry_webapi.findWidget(self.func)
        if len(self.widgetid) > 0:
            checkUUID = ryry_webapi.createTask(self.widgetid, self.params)
            checking = True
            checkCount = 0
            while checking or checkCount > 6000:
                finish, success, data = ryry_webapi.checkTask(checkUUID)
                if finish:
                    checking = False
                    if success:
                        self.call_back(self.idx, data)
                        return
                checkCount += 1
                time.sleep(0.1)
        else:
            print(f"widget {self.func}-{self.widgetid} not found")
        self.call_back(self.idx, None)

class Task:
    thread_data = {}

    def __init__(self, func: str, multi_params: list[dict], fromUUID=None, func_id=None):
        realTaskUUID = fromUUID
        if realTaskUUID == None or len(realTaskUUID) <= 0:
            realTaskUUID = taskUtils.taskInfoWithFirstTask()
            
        def _callback(idx, data):
            self.thread_data[str(idx)]["result"] = data
        idx = 0
        for param in multi_params:
            param["fromUUID"] = realTaskUUID
            self.thread_data[str(idx)] = {
                "thread" :  TaskThread(idx, func, func_id, param, _callback),
                "result" : None
            }
            idx+=1
        
    def call(self):
        for t in self.thread_data.keys():
            self.thread_data[t]["thread"].join()
        result = []
        for t in self.thread_data.keys():
            result.append(self.thread_data[t]["result"])
        return result
    
    
results = Task("Demo", [{
    "func": "你好"
}], "").call()
