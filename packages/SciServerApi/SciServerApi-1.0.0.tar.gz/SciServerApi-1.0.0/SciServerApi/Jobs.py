from SciServerApi import Authentication
import requests
import json
import time

RacmApiURL = "https://apps.sciserver.org/racm"

def getDockerComputeDomainFromName(dockerComputeDomainName):
    url = RacmApiURL + "/jobm/rest/computedomains?batch=true&interactive=false&TaskName=SciScript-Python.Jobs.getDockerComputeDomains"
    headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"}
    res = requests.get(url, headers=headers, stream=True)

    if res.status_code != 200:
        raise Exception("Error when getting Docker Compute Domains from JOBM API.\nHttp Response from JOBM API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    else:
        dockerComputeDomains = json.loads(res.content.decode())
    for dockerComputeDomain in dockerComputeDomains:
        if dockerComputeDomainName == dockerComputeDomain.get('name'):
            return dockerComputeDomain

def submitNotebookJob(notebookPath, dockerComputeDomain=None, dockerImageName=None, userVolumes=None,  dataVolumes=None, resultsFolderPath="", parameters="", jobAlias= ""):
    """
    Submits a Jupyter Notebook for execution (as an asynchronous job) inside a Docker compute domain.

    :param notebookPath: path of the notebook within the filesystem mounted in SciServer-Compute (string). Example: notebookPath = '/home/idies/worskpace/persistent/JupyterNotebook.ipynb'
    :param dockerComputeDomain: object (dictionary) that defines a Docker compute domain. A list of these kind of objects available to the user is returned by the function Jobs.getDockerComputeDomains().
    :param dockerImageName: name (string) of the Docker image for executing the notebook. E.g.,  dockerImageName="Python (astro)". An array of available Docker images is defined as the 'images' property in the dockerComputeDomain object.
    :param userVolumes: a list with the names of user volumes (with optional write permissions) that will be mounted to the docker Image. E.g.: userVolumes = [{'name':'persistent', 'needsWriteAccess':False},{'name':'scratch', , 'needsWriteAccess':True}] . A list of available user volumes can be found as the 'userVolumes' property in the dockerComputeDomain object. If userVolumes=None, then all available user volumes are mounted, with 'needsWriteAccess' = True if the user has Write permissions on the volume.
    :param dataVolumes: a list with the names of data volumes that will be mounted to the docker Image. E.g.: dataVolumes=[{"name":"SDSS_DAS"}, {"name":"Recount"}]. A list of available data volumes can be found as the 'volumes' property in the dockerComputeDomain object. If dataVolumes=None, then all available data volumes are mounted.
    :param resultsFolderPath: full path to results folder (string) where the original notebook is copied to and executed. E.g.: /home/idies/workspace/rootVolume/username/userVolume/jobsFolder. If not set, then a default folder will be set automatically.
    :param parameters: string containing parameters that the notebook might need during its execution. This string is written in the 'parameters.txt' file in the same directory level where the notebook is being executed.
    :param jobAlias: alias (string) of job, defined by the user.
    :return: the job ID (int)
    :raises: Throws an exception if the HTTP request to the Authentication URL returns an error. Throws an exception if the HTTP request to the JOBM API returns an error, or if the volumes defined by the user are not available in the Docker compute domain.
    :example: dockerComputeDomain = Jobs.getDockerComputeDomains()[0]; job = Jobs.submitNotebookJob('/home/idies/workspace/persistent/Notebook.ipynb', dockerComputeDomain, 'Python (astro)', [{'name':'persistent'},{'name':'scratch', 'needsWriteAccess':True}], [{'name':'SDSS_DAS'}], 'param1=1\\nparam2=2\\nparam3=3','myNewJob')

    """

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


    dockerComputeEndpoint = dockerComputeDomain.get('apiEndpoint');

    dockerJobModel = {
        "command": parameters,
        "scriptURI": notebookPath,
        "submitterDID": jobAlias,
        "dockerComputeEndpoint": dockerComputeEndpoint,
        "dockerImageName": dockerImageName,
        "resultsFolderURI": resultsFolderPath,
        "volumeContainers": datVols,
        "userVolumes": uVols
    }
    data = json.dumps(dockerJobModel).encode()
    
    url = RacmApiURL + "/jobm/rest/jobs/docker?TaskName=SciScript-Python.Jobs.submitNotebookJob"
    headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"}
    res = requests.post(url, data=data, headers=headers, stream=True)

    if res.status_code != 200:
        raise Exception("Error when submitting a notebook job to the JOBM API.\nHttp Response from JOBM API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    else:
        return (json.loads(res.content.decode())).get('id')


def submitShellCommandJob(shellCommand, dockerComputeDomain = None, dockerImageName = None, userVolumes = None, dataVolumes = None, resultsFolderPath = "", jobAlias = ""):
    """
    Submits a shell command for execution (as an asynchronous job) inside a Docker compute domain.

    :param shellCommand: shell command (string) defined by the user.
    :param dockerComputeDomain: object (dictionary) that defines a Docker compute domain. A list of these kind of objects available to the user is returned by the function Jobs.getDockerComputeDomains().
    :param dockerImageName: name (string) of the Docker image for executing the notebook. E.g.,  dockerImageName="Python (astro)". An array of available Docker images is defined as the 'images' property in the dockerComputeDomain object.
    :param userVolumes: a list with the names of user volumes (with optional write permissions) that will be mounted to the docker Image.
           E.g., userVolumes = [{'name':'persistent', 'needsWriteAccess':False},{'name':'scratch', , 'needsWriteAccess':True}]
           A list of available user volumes can be found as the 'userVolumes' property in the dockerComputeDomain object. If userVolumes=None, then all available user volumes are mounted, with 'needsWriteAccess' = True if the user has Write permissions on the volume.
    :param dataVolumes: a list with the names of data volumes that will be mounted to the docker Image.
           E.g., dataVolumes=[{"name":"SDSS_DAS"}, {"name":"Recount"}].
           A list of available data volumes can be found as the 'volumes' property in the dockerComputeDomain object. If dataVolumes=None, then all available data volumes are mounted.
    :param resultsFolderPath: full path to results folder (string) where the shell command is executed. E.g.: /home/idies/workspace/rootVolume/username/userVolume/jobsFolder. If not set, then a default folder will be set automatically.
    :param jobAlias: alias (string) of job, defined by the user.
    :return: the job ID (int)
    :raises: Throws an exception if the HTTP request to the Authentication URL returns an error. Throws an exception if the HTTP request to the JOBM API returns an error, or if the volumes defined by the user are not available in the Docker compute domain.
    :example: dockerComputeDomain = Jobs.getDockerComputeDomains()[0]; job = Jobs.submitShellCommandJob('pwd', dockerComputeDomain, 'Python (astro)', [{'name':'persistent'},{'name':'scratch', 'needsWriteAccess':True}], [{'name':'SDSS_DAS'}], 'myNewJob')

    .. seealso:: Jobs.submitNotebookJob, Jobs.getJobStatus, Jobs.getDockerComputeDomains, Jobs.cancelJob
    """

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
                if vol.get('name') == uVol.get('name'):
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


    dockerComputeEndpoint = dockerComputeDomain.get('apiEndpoint');

    dockerJobModel = {
        "command": shellCommand,
        "submitterDID": jobAlias,
        "dockerComputeEndpoint": dockerComputeEndpoint,
        "dockerImageName": dockerImageName,
        "volumeContainers": datVols,
        "userVolumes": uVols,
        "resultsFolderURI": resultsFolderPath
    }
    data = json.dumps(dockerJobModel).encode()
    url = RacmApiURL + "/jobm/rest/jobs/docker?TaskName=SciScript-Python.Jobs.submitShellCommandJob"
    headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"}
    res = requests.post(url, data=data, headers=headers, stream=True)

    if res.status_code != 200:
        raise Exception("Error when submitting a job to the JOBM API.\nHttp Response from JOBM API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    else:
        return (json.loads(res.content.decode())).get('id')


def getJobsList(top=10):
    url = RacmApiURL + "/jobm/rest/jobs?" + "top=" + str(top) + "&" + "TaskName=SciScript-Python.Jobs.getJobsList"
    headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"}
    res = requests.get(url, headers=headers, stream=True)
    if res.status_code != 200:
        raise Exception("Error when getting list of jobs from JOBM API.\nHttp Response from JOBM API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    else:
        return json.loads(res.content.decode())

def getJobDescription(jobId):
    """
    Gets the definition of the job,

    :param jobId: Id of job
    :return: dictionary containing the description or definition of the job.
    :raises: Throws an exception if the HTTP request to the Authentication URL returns an error, and if the HTTP request to the JOBM API returns an error.
    :example: job1 = Jobs.submitShellCommandJob(Jobs.getDockerComputeDomains()[0],'pwd', 'Python (astro)'); job2 = Jobs.getJobDescription(job1.get('id'));

    """

    url = RacmApiURL + "/jobm/rest/jobs/" + str(jobId) + "?TaskName=SciScript-Python.Jobs.getJobDescription"
    headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"}
    res = requests.get(url, headers=headers, stream=True)
    if res.status_code != 200:
        raise Exception("Error when getting from JOBM API the job status of jobId=" + str(jobId) + ".\nHttp Response from JOBM API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    else:
        return json.loads(res.content.decode())


def cancelJob(jobId):
    """
    Cancels the execution of a job.

    :param jobId: Id of the job (integer)
    :raises: Throws an exception if the HTTP request to the Authentication URL returns an error. Throws an exception if the HTTP request to the JOBM API returns an error.
    :example: job = Jobs.submitShellCommandJob(Jobs.getDockerComputeDomains()[0],'pwd', 'Python (astro)'); isCanceled = Jobs.cancelJob(job.get('id'));

    .. seealso:: Jobs.submitNotebookJob, Jobs.getJobStatus, Jobs.getDockerComputeDomains.
    """

    url = RacmApiURL + "/jobm/rest/jobs/" + str(jobId) + "/cancel?TaskName=SciScript-Python.Jobs.cancelJob"
    headers = {'X-Auth-Token': Authentication.keyToken, "Content-Type": "application/json"}
    res = requests.post(url, headers=headers, stream=True)
    if res.status_code != 200:
        raise Exception("Error when getting from JOBM API the job status of jobId=" + str(jobId) + ".\nHttp Response from JOBM API returned status code " + str(res.status_code) + ":\n" + res.content.decode());
    else:
        pass


