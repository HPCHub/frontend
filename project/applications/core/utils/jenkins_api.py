import time
from django.conf import settings
import requests
import logging
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


jenkins_base_url = '{}{}:{}@{}'.format(
    settings.JENKINS_PROTO,
    settings.JENKINS_USERNAME,
    settings.JENKINS_PASSWORD,
    settings.JENKINS_URL
)


def prepare_build(token='gcp', zone='europe-north1-a', machine_type='n1-highcpu-2', disk_size='50GB', disk_type='pd-ssd'):
    url = jenkins_base_url + '/job/gcp_single_deploy/buildWithParameters'
    params = {
        'token': token,
        'ZONE': zone,
        'MACHINE_TYPE': machine_type,
        'DISK_SIZE': disk_size,
        'DISK_TYPE': disk_type
    }
    data = requests.post(url=url, params=params)
    print(data.url)
    print(data.headers)
    location = data.headers.get('Location')
    if not location:
        logger.error('Can not request build with error {}'.format(data.headers))
    path = str(urlparse(location).path)
    time.sleep(30)
    return path


def build(path):
    url = jenkins_base_url + path + 'api/json'
    data = requests.get(url).json()
    print('build_url', url)
    print(data)
    location = data.get('executable').get('url')
    if not location:
        logger.error('Can not request build with error {}'.format(data.content))
    path = str(urlparse(location).path)
    return path

def get_build_artifacts(path):
    key_pattern = 'single-{}.key'
    ip_pattern = 'single-{}_ip'
    description = {}
    ip_path = None
    key_path = None
    url = jenkins_base_url + path + 'api/json'
    data = requests.get(url).json()
    for i in data.get('description').split(';'):
        if i:
            description.update({i.strip().split(': ')[0]: i.strip().split(': ')[1]})
    single_id = description.get('SINGLE_ID')
    artifacts = data.get('artifacts')
    for artifact in artifacts:
        if artifact.get('fileName') == key_pattern.format(single_id):
            key_path = artifact.get('relativePath')
        elif artifact.get('fileName') == ip_pattern.format(single_id):
            ip_path = artifact.get('relativePath')
    result_data = {
        'single_id': single_id,
        'ip_path': ip_path,
        'key_path': key_path,
        'artifacts': artifacts
    }
    return result_data

def get_single_artifact(path, artifact_path):
    url = jenkins_base_url + path + 'artifact/' + artifact_path
    print('artifact', url)
    data = requests.get(url)
    print(data)
    print(data.content)
    return data.text

def prepare_status_build(single_id):
    url = jenkins_base_url + '/job/gcp_single_status/buildWithParameters'
    params = {'SINGLE_ID': single_id}
    data = requests.post(url=url, params=params)
    location = data.headers.get('location')
    if not location:
        logger.error('Can not request build with error {}'.format(data.content))
    path = urlparse(location).path
    return path

def get_status_artifacts(path):
    status_pattern = 'single-{}_status'
    description = {}
    status_path = None
    url = jenkins_base_url + path + 'api/json'
    data = requests.get(url).json()
    for i in data.get('description').split(';'):
        if i:
            description.update({i.strip().split(': ')[0]: i.strip().split(': ')[1]})
    single_id = description.get('SINGLE_ID')
    artifacts = data.get('artifacts')
    for artifact in artifacts:
        if artifact.get('fileName') == status_pattern.format(single_id):
            status_path = artifact.get('relativePath')
    result_data = {
        'single_id': single_id,
        'status_path': status_path,
        'artifacts': artifacts
    }
    return result_data


def prepare_kill_build(single_id):
    url = jenkins_base_url + '/job/gcp_single_remove/buildWithParameters'
    params = {'SINGLE_ID': single_id}
    data = requests.post(url=url, params=params)
    location = data.headers.get('location')
    if not location:
        logger.error('Can not request build with error {}'.format(data.content))
    path = urlparse(location).path
    return path


def build_machine(token='gcp', zone='europe-north1-a', machine_type='n1-highcpu-2', disk_size='50GB', disk_type='pd-ssd'):
    logger.info('Starting build')
    job_path = prepare_build(token, zone, machine_type, disk_size, disk_type)
    logger.info('Job path = {}'.format(job_path))
    time.sleep(60)
    build_path = build(job_path)
    logger.info('Build path = {}'.format(build_path))
    result_data = get_build_artifacts(build_path)
    logger.info('Result = {}'.format(result_data))
    single_id = result_data.get('single_id')
    ip_data = get_single_artifact(build_path, result_data.get('ip_path'))
    key_data = get_single_artifact(build_path, result_data.get('key_path'))
    return single_id, ip_data, key_data

def kill_machine(single_id):
    logger.info('Starting kill')
    job_path = prepare_kill_build(single_id)
    logger.info('Job path = {}'.format(job_path))
    time.sleep(60)
    build_path = build(job_path)
    logger.info('Build path = {}'.format(build_path))
    result_data = get_build_artifacts(build_path)
    logger.info('Result = {}'.format(result_data))
    return result_data
