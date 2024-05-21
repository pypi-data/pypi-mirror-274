import requests
import json
import io
import subprocess

keyToken = ""

# fileSession headers = {'X-Auth-Token': Authentication.keyToken}
# jobSession headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"} stream=True

def CheckStatus(response):
    if response.status_code < 200 or response.status_code>=300:
        raise Exception("Http Response returned status code " + str(response.status_code) + ":\n" + response.content.decode())

#%% Remote file && jobs 
def login(UserName=None, Password=None):
    loginURL = "https://apps.sciserver.org/login-portal/keystone/v3/tokens?TaskName=SciScript-Python.Authentication.Login"
    authJson = {"auth":{"identity":{"password":{"user":{"name":UserName,"password":Password}}}}}
    data = json.dumps(authJson).encode()
    postResponse = requests.post(loginURL,data=data,headers={'Content-Type': "application/json"})
    keyToken  = postResponse.headers['X-Subject-Token'] if postResponse==200 else ""
    return keyToken 

def getFileServiceFromName(fileSession,fileServiceName):
    url = "https://apps.sciserver.org/racm/storem/fileservices?TaskName=SciScript-Python.Files.getFileServices"
    res = fileSession.get(url)
    CheckStatus(res)
    fileServicesAPIs = json.loads(res.content.decode())
    for fileServicesAPI in fileServicesAPIs:
        url = fileServicesAPI.get("apiEndpoint") + "api/volumes/?TaskName=SciScript-Python.Files.getFileServices"
        res = fileSession.get(url)
        CheckStatus(res)
        fileService = json.loads(res.content.decode())
        if fileServiceName == fileService.get('name'):
            return fileService

def createDir(fileSession,fileService, remotePath):
    url = fileService.get("apiEndpoint")+"api/folder/"+remotePath.strip("/")+"?quiet=True&TaskName=SciScript-Python.Files.createDir"
    res = fileSession.put(url)
    CheckStatus(res)

def dirList(fileSession,fileService, remotePath, level=1, options=''):
    url = fileService.get("apiEndpoint") + "api/jsontree/" + remotePath.strip("/") + "?options=" + options + "&level=" + str(level) + "&TaskName=SciScript-Python.Files.dirList"
    res = fileSession.get(url)
    CheckStatus(res)
    return json.loads(res.content.decode())

def delete(fileSession,fileService, remotePath):
    url = fileService.get("apiEndpoint") + "api/data/" + remotePath.strip("/") + "?quiet=True&TaskName=SciScript-Python.Files.delete"
    res = fileSession.delete(url)
    CheckStatus(res)

def upload(fileSession,fileService, remoteFilePath, localFilePath):
    url = fileService.get("apiEndpoint") + "api/file/"+remoteFilePath.strip("/")+"?quiet=True&TaskName=SciScript-Python.Files.UploadFile"
    res = fileSession.put(url, data=open(localFilePath, "rb"), stream=True)
    CheckStatus(res)

def download(fileSession,fileService, remotePath, localFilePath):
    url = fileService.get("apiEndpoint") + "api/file/"+remotePath.strip("/")+"?quiet=True&TaskName=SciScript-Python.Files.DownloadFile"
    res = fileSession.get(url, stream=True)
    CheckStatus(res)
    bytesio = io.BytesIO(res.content)
    theFile = open(localFilePath, "w+b")
    theFile.write(bytesio.read())
    theFile.close()
    return True

def getDockerComputeDomainFromName(jobSession,dockerComputeDomainName):
    url = "https://apps.sciserver.org/racm/jobm/rest/computedomains?batch=true&interactive=false&TaskName=SciScript-Python.Jobs.getDockerComputeDomains"
    res = jobSession.get(url)
    CheckStatus(res)
    dockerComputeDomains = json.loads(res.content.decode())
    for dockerComputeDomain in dockerComputeDomains:
        if dockerComputeDomainName == dockerComputeDomain.get('name'):
            return dockerComputeDomain

def submitNotebookJob(jobSession,dockerJobModel):
    url = "https://apps.sciserver.org/racm/jobm/rest/jobs/docker?TaskName=SciScript-Python.Jobs.submitNotebookJob"
    res = jobSession.post(url,data = json.dumps(dockerJobModel).encode())
    CheckStatus(res)
    return json.loads(res.content.decode())

def getJobsList(jobSession,top=10):
    url = "https://apps.sciserver.org/racm/jobm/rest/jobs?" + "top=" + str(top) + "&" + "TaskName=SciScript-Python.Jobs.getJobsList"
    res = jobSession.get(url)
    CheckStatus(res)
    return json.loads(res.content.decode())

def getJobDescription(jobSession,jobId):
    url = "https://apps.sciserver.org/racm/jobm/rest/jobs/" + str(jobId) + "?TaskName=SciScript-Python.Jobs.getJobDescription"
    res = jobSession.get(url)
    CheckStatus(res)
    return json.loads(res.content.decode())


def cancelJob(jobSession,jobId):
    url = "https://apps.sciserver.org/racm/jobm/rest/jobs/" + str(jobId) + "/cancel?TaskName=SciScript-Python.Jobs.cancelJob"
    res = jobSession.post(url)
    CheckStatus(res)

def getDockerVolumes(dockerComputeDomain, userVolumes,  dataVolumes):
    uVols = [];
    if userVolumes is None:
        for vol in dockerComputeDomain.get('userVolumes'):
            if 'write' in vol.get('allowedActions'):
                uVols.append({'userVolumeId': vol.get('id'), 'needsWriteAccess': True});
            else:
                uVols.append({'userVolumeId': vol.get('id'), 'needsWriteAccess': False});
    else:
        for uVol in userVolumes:
            found = False;
            for vol in dockerComputeDomain.get('userVolumes'):
                if vol.get('name') == uVol.get('name') and vol.get('rootVolumeName') == uVol.get('rootVolumeName') and vol.get('owner') == uVol.get('owner'):
                    found = True;
                    if (uVol.get('needsWriteAccess')):
                        if uVol.get('needsWriteAccess') == True and 'write' in vol.get('allowedActions'):
                            uVols.append({'userVolumeId': vol.get('id'), 'needsWriteAccess': True});
                        else:
                            uVols.append({'userVolumeId': vol.get('id'), 'needsWriteAccess': False});
                    else:
                        if 'write' in vol.get('allowedActions'):
                            uVols.append({'userVolumeId': vol.get('id'), 'needsWriteAccess': True});
                        else:
                            uVols.append({'userVolumeId': vol.get('id'), 'needsWriteAccess': False});

            if not found:
                raise Exception("User volume '" + uVol.get('name') + "' not found within Compute domain")

    datVols = [];
    if dataVolumes is None:
        for vol in dockerComputeDomain.get('volumes'):
            datVols.append({'name': vol.get('name')});
    else:
        for dVol in dataVolumes:
            found = False;
            for vol in dockerComputeDomain.get('volumes'):
                if vol.get('name') == dVol.get('name'):
                    found = True;
                    datVols.append({'name': vol.get('name')});

            if not found:
                raise Exception("Data volume '" + dVol.get('name') + "' not found within Compute domain")

    return uVols,datVols

### Optimized Download 

def wget(fileService, remotePath, localFilePath, **kwargs):
    proxies = kwargs.get("proxies",None)
    pollTime = kwargs.get("pollTime",0)
    wgetArgs = kwargs.get("wgetArgs","--quiet --no-clobber")
    if proxies is not None:
        proxy = f"proxy=on http_proxy={proxies['http']} https_proxy={proxies['http']}"
    else:
        proxy = ""

    url = fileService.get("apiEndpoint") + "api/file/" + remotePath.strip("/") + "?TaskName=SciScript-Python.Files.DownloadFile"
    headers = f"X-Auth-Token: {keyToken}"

    cmd = proxy + f"sleep {pollTime} && wget \"{url}\" --header \"{headers}\" --output-document \"{localFilePath}\" {wgetArgs}"
    
    return subprocess.Ppoen(cmd,shell=True)
    
