from django.test import TestCase, Client
from account.models import CustomUser
from core.models import CompanySheet, Company, MainDomain, SubDomain, Prefecture
from core.tests import create_userdata
import json


class GetCompanyListApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def setUp(self):
        sheet = create_userdata()
        user = CustomUser.objects.create(username="test_user", email="example@test.com", password="test")
        user.company.add(sheet)
        user.save()
        self.client.force_login(user)

    def test_get_companies(self):
        res = self.client.get("/api/company_list")
        res = json.loads(res.content)

        expect = {"status": True,
                  "company": [{"company_id": "test1234", "name": "Test inc.", "year_founded": "2020-09-17",
                               "capital": 500, "revenue": 100, "employee": 100, "ave_age": 36.5,
                               "grad_hire_last_year": 10, "working_time_start": "22:19:40",
                               "working_time_end": "22:19:40", "salary": 50000, "benefit": "", "motto": "",
                               "business": "", "main_domain": "IT", "sub_domain": ["Software", "Mobile App"],
                               "prefecture": ["Tokyo", "Osaka"], "strength": "Strength",
                               "weakness": "", "interested": "", "impression": ""}]}
        self.assertDictEqual(res, expect)
