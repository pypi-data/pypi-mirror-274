import json, os
import datetime
import uuid, requests
import calendar, time

from ryry import store 
from ryry import utils 
from ryry import taskUtils 
from ryry import constant 

def _aigc_post(func, params, files={}, timeout=10):
    s = requests.session()
    try:
        requests.adapters.DEFAULT_RETRIES = 2
        s.keep_alive = False
        s.headers.update({'Connection':'close'})
        s.headers.update({'Usertoken':"0cce7cfe3629e16ee9b3ea8563305d3a15c524804da1861db07c2c867d79da63"})
        if len(files) <= 0:
            s.headers.update({'Content-Type':'application/json'})
        res = s.post(url=f"https://api.dalipen.com/{func}", json=params, files=files, timeout=timeout, verify=False)
        if res.status_code == 200:
            result_data = json.loads(res.content)
            res.close()
            if result_data["code"] == 0:
                return 0, "", result_data["data"]
            else:
                return result_data["code"], result_data["msg"], ""
        else:
            raise Exception(f'''request {func} status_code={res.status_code}''')
    except Exception as e:
        taskUtils.taskPrint(None, f'''=============== ryry {func} server error {datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')} ===============
url={func}

req=
{params}
exception={e}
===============
''')
        return -1, str(e), ""
    finally:
        s.close()
    return -1, "", ""
    
#======================================== Task Function ==============================
def _extend():
    extInfo = store.readDeviceInfo()
    extInfo["app_version"] = constant.app_version
    extInfo["app_bulld_number"] = constant.app_bulld_number
    extInfo["app_name"] = constant.app_name
    extInfo["dts"] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
    extInfo["trace_id"] = ''.join(str(uuid.uuid4()).split('-'))
    extInfo["host_name"] = utils.get_hostname()
    return json.dumps(extInfo)

def GetTask():
    widget_map = ["TESTTEST"]
    map = store.widgetMap()
    for it in map:
        if isinstance(map[it], (dict)):
            if map[it]["isBlock"] == False:
                widget_map.append(it)
        else:
            widget_map.append(it)
    req = {
        "widget_map": json.dumps(widget_map),
        "limit": 1,
    }
    r1, r2, r3 = _aigc_post("aigc/task/getTask", req)
    if r1 != 0:
        return [], 10
    datas = []
    for it in r3:
        datas.append({
            "taskUUID": it["task_uuid"],
            "config": it["config"],
            "data": it["data"],
        })
    #Previous tasks may have failed due to network problems, so collect and resend
    retryLastTaskNotify()
    return datas, 600

TASK_NOTIFY_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"task_notify_data.json")
def saveTaskNotifyData(taskUUID, status, msg, dataStr):
    taskUtils.taskPrint(taskUUID, f"save {taskUUID} to next notify")
    data = []
    try:
        if not os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'w') as f:
                json.dump([], f)
        with open(TASK_NOTIFY_DATA, 'r') as f:
            data = json.load(f)
    except:
        pass
    try:
        data.append({
            "taskUUID":taskUUID,
            "status":status,
            "msg":msg,
            "dataStr":dataStr,
            "pts": calendar.timegm(time.gmtime())
        })
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(data, f)
    except:
        pass
def resetLastTaskNotify(taskUUID):
    data = []
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r') as f:
                data = json.load(f)
    except:
        pass
    try:
        newData = []
        for it in data:
            if it["taskUUID"] != taskUUID:
                newData.append(it)
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(newData, f)
    except:
        pass
def retryLastTaskNotify():
    data = []
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r') as f:
                data = json.load(f)
    except:
        pass
    try:
        newData = []
        for it in data:
            msg = it["msg"]
            fail_count = 0
            if "fail_count" in it:
                fail_count = it["fail_count"]
            else:
                it["fail_count"] = 0
            pts = 0
            if "pts" in it:
                pts = it["pts"]
            if abs(calendar.timegm(time.gmtime())-pts) < 10: #notify late after 10 sec
                newData.append(it)
                continue
            if fail_count < 10:
                if TaskNotify(it["taskUUID"], it["status"], f"{msg} *", it["dataStr"], False) == False:
                    it["fail_count"] += 1
                    newData.append(it)
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(newData, f)
    except:
        pass
def TaskNotify(taskUUID, status, msg, dataStr, failSaveNotify=True):
    req = {
        "task_uuid": taskUUID,
        "status": status,
        "msg": msg,
        "dataStr": dataStr
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskNotify", req)
    if r1 != 0:
        if failSaveNotify:
            #tasks may have failed due to network problems, so collect and resend
            saveTaskNotifyData(taskUUID, status, msg, dataStr)
        return False
    return r3
  
retryLastTaskNotify()
def TaskUpdateProgress(taskUUID, progress, dataStr):
    # req = aigc_ext_pb2.TaskUpdateReq()
    # req.taskUUID = taskUUID
    # req.progress = progress
    # req.data = dataStr
    
    # rsp = aigc_ext_pb2.TaskUpdateRes()
    # r1, r2, r3 = _aigc_post(req, "TaskUpdate")
    # if r1 != 0:
    #     return False
    # rsp.ParseFromString(r3)
    return True

def upload(localFilePath, ext):
    with open(localFilePath, "rb") as f:
        files = { 'file':f }
        params = { 'ext':ext }
        r1, r2, r3 = _aigc_post("upload/create", params, files=files,timeout=100)
    if r1 != 0:
        raise Exception(f"upload fail!, reason={r2}")
    return r3

def uploadWidget(widget_id, name, whl, ext, version):
    with open(whl, "rb") as f:
        files = { 'file':f }
        params = {
            'widget_id':widget_id,
            'name':name,
            'version':version,
            'ext':ext
        }
        r1, r2, r3 = _aigc_post("aigc/task/publishWidget", params, files=files, timeout=100)
    if r1 != 0:
        raise Exception(f"upload fail!, reason={r2}")
    return r3

def CreateWidgetUUID():
    req = {}
    r1, r2, r3 = _aigc_post("aigc/task/createWidget", req)
    if r1 != 0:
        raise Exception(f"CreateWidgetUUID fail!, reason={r2}")
    return r3

#======================================== Task Function ==============================
def createTask(widget_id, params):
    req = {
        "widget_id": widget_id,
        "widget_data": json.dumps(params),
        "extend": _extend()
    }
    r1, r2, r3 = _aigc_post("aigc/task/createTask", req)
    if r1 != 0:
        raise Exception(f"create task fail!, reason={r2}")
    return r3

def findWidget(name):
    req = {
        "name": name
    }
    r1, r2, r3 = _aigc_post("aigc/task/findWidget", req)
    if r1 != 0:
        return 0
    for it in r3:
        widget_id = it["widget_id"]
        widget_name = it["name"]
        if widget_name.strip().lower() == name.strip().lower():
            return widget_id
    return 0

def checkTask(checkUUID):
    req = {
        "task_uuid": checkUUID
    }
    r1, r2, r3 = _aigc_post("aigc/task/checkTask", req)
    if r1 != 0:
        return False, False, "server fail"
    if r3["status"] < 3:
        return False, False, ""
    elif r3["status"] == 3:
        return True, True, json.loads(r3["task_result"])
    elif r3["status"] == 4:
        return True, False, r3["fail_reason"]