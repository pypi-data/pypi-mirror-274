import json

from importers.common.http_util import send_graphql_post, get_token


# 获取custom_events表(id,key,name,description)数据
def getdataCenterCustomEvents(token=get_token()):
    """
        获取 CustomEvents (id,key,name,description)
    """
    body = """{"query":"query MyQuery {  dataCenterCustomEvents {    id   key   name   description}}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    data_info = content['dataCenterCustomEvents']
    return data_info


def getdataCenterCustomEventsAndAttr(token=get_token()):
    """
        获取 CustomEvents (id,key,name,description,attributes(id,key))
    """
    body = """{"query":"query MyQuery {  dataCenterCustomEvents {    id   key   name   description   attributes {id  key}}}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    data_info = content['dataCenterCustomEvents']
    return data_info


def getdataCenterUserVariables(token=get_token()):
    """
        获取 UserVariables (id,key,name,description,valueType)
    """
    body = """{"query":"query MyQuery {  dataCenterUserVariables {    id   key   name   description   valueType}}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    data_info = content['dataCenterUserVariables']
    return data_info


def getdataCenterEventVariables(token=get_token()):
    """
        获取 EventVariables (id,key,name,description,valueType)
    """
    body = """{"query":"query MyQuery {dataCenterEventVariables {    id   key   name   description   valueType}}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    data_info = content['dataCenterEventVariables']
    return data_info


# 获取元数据
def getMetaData(token=get_token()):
    """
        获取元数据
    """
    body = """{"query":"query MyQuery {dataCenterCustomEvents {    key    name    description  }  dataCenterEventVariables {    key    name    
    valueType    description  }  dataCenterUserVariables {    key    name    valueType    description  }}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    data_info = content
    return data_info


def getBindEvent(token=get_token()):
    """
        获取绑定事件和关联事件属性
    """
    body = """{"query":"query MyQuery {  dataCenterCustomEvents {    key    attributes {      key    }  }}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    data_info = content
    return data_info


def getTunnels(token=get_token()):
    """
        获取 tunnels(id  key   type   config)
    """
    body = """{"query":"query MyQuery { tunnels {id  key   type   config  }}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    tunnels = content['tunnels']
    t_res = {}
    for t in tunnels:
        res = {}
        if t['type'] == 'FILE':
            res[eval(t['config'])['type']] = t['id']
            t_res[t['key']] = res
    return t_res


def getClearUsers(token=get_token()):
    """
        获取待删除用户列表
    """
    body = """{"query":"query MyQuery {clearUsers {id projectId stage}}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    clearusers = content['clearUsers']
    res = {}
    for user in clearusers:
        if (user['stage'] == 'WAITING'):
            res[user['id']] = str(user['projectId'])
    return res


def getGidByUserId(userid, token=get_token()):
    """
        获取用户ID对应Gid
    """
    body = """{
        "operationName":"getGidByUser",
        "variables":{
            "userId":"%s"
        },
        "query":"query getGidByUser($userId: String!) {
          getGidByUser(userId: $userId) 
            }
        "}
    """ % (userid)
    content = send_graphql_post(token, body)
    return content['getGidByUser']


def getGidAllData(gid, token=get_token()):
    """
        获取Gid下所有埋点、用户属性数据
    """
    body = """{
        "operationName":"getAllUserData",
        "variables":{
            "gioId":"%s"
        },
        "query":"query getAllUserData($gioId: Long!) {
            getAllUserData(gioId: $gioId)
        }
    "}
    """ % (gid)
    content = send_graphql_post(token, body)
    return content['getAllUserData']


def updateClearUserJobStatus(id, token=get_token()):
    """
        更新待删除用户状态
    """
    body = """{
        "operationName":"updateClearUser",
        "variables":{
            "id":"%s",
            "clearUser":{
                "stage":"RUNNING"
            }
        },
        "query":"mutation updateClearUser($id: HashId!,$clearUser:ClearUserInput!) {
            updateClearUser(id:$id,clearUser:$clearUser) {
                stage
            }
        }
    "}
    """ % (id)
    content = send_graphql_post(token, body)
    return content['updateClearUser']['stage']


def deleteClearUserData(gid, token=get_token()):
    """
        删除Gid下埋点、用户属性数据
    """
    body = """{
        "operationName":"deleteClearUserData",
        "variables":{
           "gioId":"%s"
        },
        "query":"mutation deleteClearUserData($gioId: Long!) {
            deleteClearUserData(gioId: $gioId)
        }
    "}
    """ % (gid)
    content = send_graphql_post(token, body)
    return content['deleteClearUserData']


def checkUserExits(userid, token=get_token()):
    """
        检查用户是否存在
    """
    body = """{
        "operationName":"checkUserExists",
        "variables":{
            "clearUserId":"%s"
        },
        "query":"query checkUserExists($clearUserId: String!) {
            checkUserExists(clearUserId: $clearUserId)
        }
    "}
    """ % (userid)
    content = send_graphql_post(token, body)
    return content['checkUserExists']


def createClearUser(userid, token=get_token()):
    """
        添加待删除用户
    """
    body = """{
        "operationName":"createClearUser",
        "variables":{
            "clearUser":{
            "userId":"%s"
            }
        },
        "query":"mutation createClearUser($clearUser: ClearUserInput!) {
        createClearUser(clearUser: $clearUser) {
           id   userId   stage    __typename 
         }
        }
    "}
    """ % (userid)
    content = send_graphql_post(token, body)
    return content['createClearUser']


def trigger_job(id, token=get_token()):
    """
      触发任务
    """
    body = '''{
      "operationName":"executeJob",
      "variables":{"id":"%s"},
      "query":"mutation executeJob($id: HashId!) {  
        executeJob(id: $id) {
            id    
            stage    
            __typename  
        }
      }"
    }''' % id
    send_graphql_post(token, body)


def getImportJobStatus(id, token=get_token()):
    body = """{"query":"query MyQuery {  eventImportJobs {  id  name   stage }}","variables":null,"operationName":"MyQuery"}"""
    content = send_graphql_post(token, body)
    eventImportJobs = content['eventImportJobs']
    stage = ''
    for jobs in eventImportJobs:
        if jobs['id'] == id:
            stage = jobs['stage']
    if stage is not None and (stage.__eq__("FINISH") or stage.__eq__("ERROR")):
        return True
    else:
        return False


def getdataCenterItemModels(token=get_token()):
    """
        获取 ItemVariables (id,key,name,isPrimaryKey,updatedAt)
    """
    body = """{"operationName":"dataCenterItemModels","variables":{},"query":"query dataCenterItemModels {\n  dataCenterItemModels {\n    id\n    name\n    creator\n    creatorId\n    createdAt\n    updater\n    updaterId\n    updatedAt\n    description\n    eventVariableId\n    attributes {\n      id\n      name\n      key\n      valueType\n      isPrimaryKey\n    description\n      updatedAt\n      __typename\n    }\n    __typename\n  }\n}\n"}"""
    content = send_graphql_post(token, body)
    data_info = content['dataCenterItemModels']
    return data_info
