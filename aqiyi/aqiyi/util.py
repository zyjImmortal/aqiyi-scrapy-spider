import hashlib
import traceback

import oss2 as oss
import requests
from scrapy.utils.project import get_project_settings

AccessKeyId=get_project_settings().get('ACCESSKEYID')
AccessKeySecret=get_project_settings().get('ACCESSKEYSECRET')
Endpoint=get_project_settings().get('ENDPOINT')
BUCKET=get_project_settings().get('BUCKET')
bucket = oss.Bucket(oss.Auth(AccessKeyId, AccessKeySecret), Endpoint, BUCKET)


def upload(url,folder=None):
    if url==None:
        return None
    try:
        m = hashlib.md5()
        m.update(url.encode('UTF-8'))
        filename=m.hexdigest()
        input = requests.get(url)
        result = bucket.put_object(folder+'/' + filename + '.jpg', input)
        if result.status == 200:
            return "https://"+BUCKET+"."+Endpoint+"/"+folder+"/"+filename+".jpg"
        else:
            return None
    except:
        traceback.print_exc()
        return None