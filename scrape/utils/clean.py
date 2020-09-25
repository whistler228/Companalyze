from django.utils.timezone import datetime
from core.models import MainDomain, SubDomain, Prefecture
import re


def clean_year_founded(string):
    year = re.search(r"([0-9]{4})年", string)
    month = re.search(r"([0-9]{1,2})月", string)
    if year:
        if month:
            date = datetime.strptime("-".join([year.group(1), month.group(1)]), "%Y-%m")
        else:
            date = datetime.strptime(year.group(1), "%Y")
        return date
    else:
        return None


def clean_employee(string):
    n = re.search(r"([0-9]+?)[名|人]", string)
    if n:
        return int(n.group(1))


def clean_sub_domain(sd_list):
    return [SubDomain.objects.get_or_create(name=sd)[0] for sd in sd_list]


def clean_main_domain(main_domain):
    return MainDomain.objects.get_or_create(name=main_domain)[0]


def clean_prefecture(prefectures):
    return [Prefecture.objects.get_or_create(name=pf)[0] for pf in prefectures]
