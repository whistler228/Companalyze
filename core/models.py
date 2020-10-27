from django.db import models
from django.forms.models import model_to_dict

from account.models import CustomUser


class Company(models.Model):
    company_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=120)
    main_domain = models.ForeignKey("MainDomain", on_delete=models.CASCADE, related_name="main_domain")
    sub_domain = models.ManyToManyField("SubDomain", related_name="sub_domain")
    year_founded = models.DateField(null=True)
    capital = models.CharField(max_length=100, null=True)
    revenue = models.CharField(max_length=100, null=True)
    employee = models.CharField(max_length=100, null=True)
    ave_age = models.CharField(max_length=100, null=True)
    grad_hire_last_year = models.CharField(max_length=100, null=True)
    prefectures = models.ManyToManyField("Prefecture", related_name="companies")
    offices = models.CharField(max_length=1000, null=True)
    working_time = models.CharField(max_length=300, null=True)
    salary = models.CharField(max_length=100, null=True)
    benefit = models.CharField(max_length=2000, null=True)
    motto = models.CharField(max_length=2000, null=True)
    business = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        d = model_to_dict(self, exclude=["main_domain", "sub_domain", "prefectures"])
        main_domain = {"main_domain": self.main_domain.name}
        sub_domain = {"sub_domain": [sd.name for sd in self.sub_domain.all()]}
        prefecture = {"prefecture": [pf.name for pf in self.prefectures.all()]}
        return {**d, **main_domain, **sub_domain, **prefecture}


class CompanySheet(models.Model):
    company_id = models.CharField(max_length=10)
    name = models.CharField(max_length=120)
    main_domain = models.ForeignKey("MainDomain", on_delete=models.CASCADE, related_name="cs_main_domain")
    sub_domain = models.ManyToManyField("SubDomain", related_name="cs_sub_domain")
    company_url = models.CharField(max_length=120, null=True)
    prefectures = models.ManyToManyField("Prefecture", related_name="cs_companies")
    year_founded = models.DateField(null=True)
    capital = models.BigIntegerField(null=True)
    revenue = models.BigIntegerField(null=True)
    employee = models.IntegerField(null=True)
    ave_age = models.FloatField(null=True)
    grad_hire_last_year = models.IntegerField(null=True)
    working_time_start = models.TimeField(null=True)
    working_time_end = models.TimeField(null=True)
    salary = models.IntegerField(null=True)
    benefit = models.CharField(max_length=1000, null=True)
    motto = models.CharField(max_length=1000, null=True)
    business = models.CharField(max_length=1000, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_sheet")
    # get reverse by companySheet.created_by.created_sheet.all()

    strength = models.CharField(max_length=1000, blank=True)
    weakness = models.CharField(max_length=1000, blank=True)

    interested = models.CharField(max_length=1000, blank=True)
    impression = models.CharField(max_length=1000, blank=True)

    note = models.CharField(max_length=2000, blank=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company_id", "created_by"),)

    def to_dict(self):
        d = model_to_dict(self, exclude=["id", "main_domain", "sub_domain", "prefectures", "created_by"])
        main_domain = {"main_domain": self.main_domain.name}
        sub_domain = {"sub_domain": [sd.name for sd in self.sub_domain.all()]}
        prefecture = {"prefecture": [pf.name for pf in self.prefectures.all()]}
        return {**d, **main_domain, **sub_domain, **prefecture}


class MainDomain(models.Model):
    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.name


class SubDomain(models.Model):
    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.name


class Prefecture(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
