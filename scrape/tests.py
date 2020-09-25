from django.test import TestCase
from .get_company import get_company


class GetCompanyDataTests(TestCase):
    def test_rikunabi(self):
        company_id = "r674122088"
        res = get_company(company_id)
        print(res)
        self.assertTrue(res)
