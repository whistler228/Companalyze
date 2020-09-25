from django.test import TestCase
from django.utils.timezone import datetime
from .models import *


class CompanyTests(TestCase):
    def setUp(self):
        create_userdata()

    def test_to_dict(self):
        res = CompanySheet.objects.first().to_dict()
        print(res)

        explain = {"company_id": "test1234", "name": "Test inc.",
                   "year_founded": datetime.strptime("2020-09-17", "%Y-%m-%d").date(), "capital": 500, "revenue": 100,
                   "employee": 100, "ave_age": 36.5, "grad_hire_last_year": 10,
                   "working_time_start": datetime.strptime("22:19:40", "%H:%M:%S").time(),
                   "working_time_end": datetime.strptime("22:19:40", "%H:%M:%S").time(), "salary": 50000, "benefit": "",
                   "motto": "", "business": "", "main_domain": "IT", "sub_domain": ["Software", "Mobile App"],
                   "prefecture": ["Tokyo", "Osaka"], "strength": "Strength",
                   "weakness": "", "interested": "", "impression": ""}
        self.assertDictEqual(explain, res)


def create_userdata():
    user = CustomUser.objects.create(username="test_user", email="test@gmail.com", password="this_is_test",
                                     nickname="test")
    main_domain = MainDomain.objects.create(name="IT")
    sub_domains = [SubDomain.objects.create(name="Software").id, SubDomain.objects.create(name="Mobile App").id]
    prefectures = [Prefecture.objects.create(name="Tokyo").id, Prefecture.objects.create(name="Osaka").id]
    c = Company.objects.create(
        company_id="test1234", name="Test inc.", year_founded="2020-09-17", capital="500",
        revenue="100", employee="100", ave_age="36.5", grad_hire_last_year="10", working_time="22:19:40 ~ 22:19:40",
        salary="50000", benefit="", motto="", business="", main_domain=main_domain
    )
    [c.sub_domain.add(sd_id) for sd_id in sub_domains]
    [c.prefectures.add(p) for p in prefectures]
    c.save()
    s = CompanySheet.objects.create(company=c, strength="Strength", weakness="", interested="",
                                    impression="", created_by=user)
    return s
