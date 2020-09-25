import requests
from lxml import etree
import string
import random


def tree_from_rikunabi_api(company_id):
    url = 'https://job.rikunabi.com/api/2022/company/top/'
    data = {'nonmember_token': '22RN_aQwpGACawy', 'time_stamp': '20200919185357', 'application_version': '2.1.1',
            'os_version': '5.1.1', 'kokyaku_cd': company_id}
    res = requests.post(url, data)
    res.raise_for_status()
    xml = res.text.encode("utf-8")
    tree = etree.fromstring(xml)
    return tree
