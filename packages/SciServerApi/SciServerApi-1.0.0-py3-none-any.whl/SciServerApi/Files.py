from SciServerApi import Authentication
import requests
import json
from io import BytesIO
import subprocess

RacmApiURL = "https://apps.sciserver.org/racm"

def getFileServices():
    """
    Gets the definitions of file services that a user is able to access. A FileService represents a file system that contains root volumes accessible to the user for public/private data storage. Within each rootVolume, users can create sharable userVolumes for storing files.

    :param verbose: boolean parameter defining whether warnings will be printed (set to True) or not (set to False).
    :return: list of dictionaries, where each dictionary represents the description of a FileService that the user is able to access.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the RACM API returns an error.
    :example: fileServices = Files.getFileServices();

    """
    url = RacmApiURL + "/storem/fileservices?TaskName=SciScript-Python.Files.getFileServices"
    headers = {'X-Auth-Token': Authentication.keyToken}

    res = requests.get(url, headers=headers)

    if res.status_code >= 200 and res.status_code < 300:
        fileServices = [];
        fileServicesAPIs = json.loads(res.content.decode())
        for fileServicesAPI in fileServicesAPIs:
            url = fileServicesAPI.get("apiEndpoint") + "api/volumes/?TaskName=SciScript-Python.Files.getFileServices"
            res = requests.get(url, headers=headers)
            if res.status_code >= 200 and res.status_code < 300:
                fileServices.append(json.loads(res.content.decode()))
        return fileServices;
    else:
        raise Exception("Error when getting the list of FileServices.\nHttp Response from FileService API returned status code " + str(res.status_code) + ":\n" + res.content.decode());

def getFileServiceFromName(fileServiceName):
    fileServices = getFileServices()
    for fileService in fileServices:
        if fileServiceName == fileService.get('name'):
            return fileService

def createDir(fileService, path):
    """
    Create a directory.

    :param fileService: name of fileService (string), or object (dictionary) that defines a file service. A list of these kind of objects available to the user is returned by the function Files.getFileServices().
    :param path: path (in the remote file service) to the directory (string), starting from the root volume level or data volume level. Examples: rootVolume/userVolumeOwner/userVolume/directory or dataVolume/directory
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the FileService API returns an error.
    :example: fileServices = Files.getFileServices(); Files.createDir(fileServices[0], "Storage/myUserName/persistent/myNewDir");

    """
    
    url = fileService.get("apiEndpoint").rstrip("/")+"/api/folder/"+path.strip("/")+"?quiet=True&TaskName=SciScript-Python.Files.createDir"
    headers = {'X-Auth-Token': Authentication.keyToken}

    res = requests.put(url, headers=headers)
    if res.status_code >= 200 and res.status_code < 300:
        pass
    else:
        raise Exception("Error when creating directory '" + str(path) + "' in file service '" + str(fileService.get('name')) + "'.\nHttp Response from FileService API returned status code " + str(res.status_code) + ":\n" + res.content.decode());


def dirList(fileService, path, level=1, options=''):
    """
    Lists the contents of a directory.

    :param fileService: name of fileService (string), or object (dictionary) that defines a file service. A list of these kind of objects available to the user is returned by the function Files.getFileServices().
    :param path: String defining the path (in the remote file service) of the directory to be listed, starting from the root volume level or data volume level. Examples: rootVolume/userVolumeOwner/userVolume/directoryToBeListed or dataVolume/directoryToBeListed
    :param level: amount (int) of listed directory levels that are below or at the same level to that of the relativePath.
    :param options: string of file filtering options.
    :return: dictionary containing the directory listing.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the FileService API returns an error.
    :example: fileServices = Files.getFileServices(); dirs = Files.dirList(fileServices[0], "Storage/myUserName/persistent/", level=2);

    """
    url = fileService.get("apiEndpoint").rstrip("/") + "/api/jsontree/" + path.strip("/") + "?options=" + options + "&level=" + str(level) + "&TaskName=SciScript-Python.Files.dirList"
    headers = {'X-Auth-Token': Authentication.keyToken}
    
    res = requests.get(url, headers=headers)

    if res.status_code >= 200 and res.status_code < 300:
        return json.loads(res.content.decode());
    else:
        raise Exception("Error when listing contents of '" + str(path) + "'.\nHttp Response from FileService API returned status code " + str(res.status_code) + ":\n" + res.content.decode());

def delete(fileService, path):
    """
    Deletes a directory or file in the File System.

    :param fileService: name of fileService (string), or object (dictionary) that defines a file service. A list of these kind of objects available to the user is returned by the function Files.getFileServices().
    :param path: String defining the path (in the remote fileService) of the file or directory to be deleted, starting from the root volume level or data volume level. Examples: rootVolume/userVolumeOwner/userVolume/fileToBeDeleted.txt or dataVolume/fileToBeDeleted.txt
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the FileService API returns an error.
    :example: fileServices = Files.getFileServices(); Files.delete(fileServices[0], "Storage/myUserName/persistent/myUselessFile.txt");

    """

    url = fileService.get("apiEndpoint").rstrip("/") + "/api/data/" + path.strip("/") + "?quiet=True&TaskName=SciScript-Python.Files.delete"
    headers = {'X-Auth-Token': Authentication.keyToken}

    res = requests.delete(url, headers=headers)
    if res.status_code >= 200 and res.status_code < 300:
        pass;
    else:
        raise Exception("Error when deleting '" + str(path) + "'.\nHttp Response from FileService API returned status code " + str(res.status_code) + ":\n" + res.content.decode());


def upload(fileService, path, localFilePath):
    """
    Uploads data or a local file into a path defined in the file system.

    :param fileService: name of fileService (string), or object (dictionary) that defines a file service. A list of these kind of objects available to the user is returned by the function Files.getFileServices().
    :param path: path (in the remote file service) to the destination file (string), starting from the root volume level or data volume level. Examples: rootVolume/userVolumeOwner/userVolume/destinationFile.txt or dataVolume/destinationFile.txt
    :param localFilePath: path to a local file to be uploaded (string),
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the FileService API returns an error.
    :example: fileServices = Files.getFileServices(); Files.upload(fileServices[0], "myRootVolume/myUserName/myUserVolume/myUploadedFile.txt", None, localFilePath="/myFile.txt");

    """

    url = fileService.get("apiEndpoint").rstrip("/")+"/api/file/"+path.strip("/")+"?quiet=True&TaskName=SciScript-Python.Files.UploadFile"
    headers = {'X-Auth-Token': Authentication.keyToken}
    with open(localFilePath, "rb") as file:
        res = requests.put(url, data=file, headers=headers, stream=True)

    if res.status_code >= 200 and res.status_code < 300:
        pass
    else:
        raise Exception("Error when uploading file to '" + str(path) + "' in file service '" + str(fileService.get('name')) + "'.\nHttp Response from FileService API returned status code " + str(res.status_code) + ":\n" + res.content.decode());



def download(fileService, path, localFilePath,**kwargs):
    """
    Downloads a file from the remote file system into the local file system, or returns the file content as an object in several formats.

    :param fileService: name of fileService (string), or object (dictionary) that defines a file service. A list of these kind of objects available to the user is returned by the function Files.getFileServices().
    :param path: String defining the path (in the remote file service) of the file to be downloaded, starting from the root volume level or data volume level. Examples: rootVolume/userVolumeOwner/userVolume/fileToBeDownloaded.txt or dataVolume/fileToBeDownloaded.txt
    :param localFilePath: local destination path of the file to be downloaded. If set to None, then an object of format 'format' will be returned.
    :return: If the 'localFilePath' parameter is defined, then it will return True when the file is downloaded successfully in the local file system. If the 'localFilePath' is not defined, then the type of the returned object depends on the value of the 'format' parameter (either io.StringIO, io.BytesIO, requests.Response or string).
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the FileService API returns an error.
    :example: fileServices = Files.getFileServices(); Files.upload(fileServices[0], "Storage/myUserName/persistent/fileToBeDownloaded.txt", localFilePath="/fileToBeDownloaded.txt");

    """
    proxies = kwargs.get("proxies",{"http": "http://127.0.0.1:7890","https": "http://127.0.0.1:7890"})
    
    url = fileService.get("apiEndpoint").rstrip("/")+"/api/file/"+path.strip("/")+"?quiet=True&TaskName=SciScript-Python.Files.DownloadFile"
    headers = {'X-Auth-Token': Authentication.keyToken}

    res = requests.get(url, stream=True, headers=headers,proxies = proxies)
    if res.status_code < 200 or res.status_code >= 300:
        raise Exception("Error when downloading '" + str(path) + "' from file service '" + str(fileService.get("name")) + "'.\nHttp Response from FileService API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    bytesio = BytesIO(res.content)
    theFile = open(localFilePath, "w+b")
    theFile.write(bytesio.read())
    theFile.close()
    return True


def wget(fileService, path, localFilePath, **kwargs):
    proxies = kwargs.get("proxies",{"http": "http://127.0.0.1:7890","https": "http://127.0.0.1:7890"})
    asyncArgs = kwargs.get("asyncArgs",False)
    wgetArgs = kwargs.get("wgetArgs","--quiet --no-clobber")

    url = fileService.get("apiEndpoint").rstrip("/") + "/api/file/" + path.strip("/") + "?TaskName=SciScript-Python.Files.DownloadFile"
    headers = {'X-Auth-Token': Authentication.keyToken}

    cmd = f"proxy=on http_proxy={proxies['http']} https_proxy={proxies['http']} wget \"{url}\" --header \'{headers}\' --output-document \"{localFilePath}\" {wgetArgs} "
    
    if asyncArgs:
        pipe = subprocess.run(cmd,shell=True)
        return pipe.returncode
    else:
        return subprocess.Ppoen(cmd,shell=True)
    
