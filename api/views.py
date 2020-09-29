from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError

from account.models import CustomUser
from core.models import Company, CompanySheet, MainDomain, SubDomain, Prefecture
from scrape.get_company import get_company

from logging import getLogger

logger = getLogger(__name__)


@login_required
def get_sheet_list(request):
    user = get_object_or_404(CustomUser, username=request.user.username)
    res = []
    for c in user.created_sheet.all():
        res.append(c.to_dict())
    return JsonResponse({"status": True, "company": res})


@login_required
def get_sheet_detail(request):
    company_id = request.GET.get("companyId")
    if not company_id:
        return JsonResponse({"status": False})
    user = get_object_or_404(CustomUser, username=request.user.username)
    sheet = user.created_sheet.filter(company_id=company_id).first()
    sheet = sheet.to_dict()
    return JsonResponse({"status": True, "detail": sheet})


@login_required
def get_company_data(request):
    company_id = request.GET.get("companyId")
    if not company_id:
        return JsonResponse({"status": False})
    company = Company.objects.filter(company_id=company_id).first()
    if company:
        return JsonResponse({"status": True, "data": company.to_dict()})
    else:
        data = get_company(company_id)
        company = Company.objects.create(
            company_id=company_id,
            name=data["name"],
            main_domain=data["main_domain"],
            year_founded=data["year_founded"],
            capital=data["capital"],
            employee=data["employee"],
            offices=data["offices"],
            ave_age=data["ave_age"],
            motto=data["motto"],
            business=data["business"],
            grad_hire_last_year=data["grad_hire_last_year"],
            working_time=data["working_time"],
            benefit=data["benefit"]
        )
        [company.sub_domain.add(sd.id) for sd in data["sub_domains"]]
        [company.prefectures.add(pf.id) for pf in data["prefectures"]]
        company.save()

        logger.info(f"[{__name__}] Create - {company_id}")
        return JsonResponse({"status": True, "data": company.to_dict()})
        # except IntegrityError:
        #     logger.error(f"{__name__}, {company_id}")


@login_required
def add_sheet(request):
    user = get_object_or_404(CustomUser, username=request.user.username)
    data = request.POST
    name = data.get("name")
    company_id = data.get("company_id")
    main_domain = MainDomain.objects.get_or_create(name=data.get("main_domain"))[0]
    sub_domain = [SubDomain.objects.get_or_create(name=x)[0] for x in data.getlist("sub_domain")]
    year_founded = data.get("year_founded") + "-01" if data.get("year_founded") else None
    employee = int(data.get("employee")) if data.get("employee") else None
    capital = int(data.get("capital")) if data.get("capital") else None
    revenue = int(data.get("revenue")) if data.get("revenue") else None
    working_time_start = data.get("working_time_start") if data.get("working_time_start") else None
    working_time_end = data.get("working_time_end") if data.get("working_time_end") else None
    offices = [Prefecture.objects.get_or_create(name=x)[0] for x in data.getlist("offices")]
    salary = int(data.get("salary")) if data.get("salary") else None
    benefit = data.get("benefit")
    motto = data.get("motto")
    business = data.get("business")
    note = data.get("note")

    sheet, _ = CompanySheet.objects.update_or_create(
        company_id=company_id,
        created_by=user,
        defaults={
            "name": name,
            "main_domain": main_domain,
            "year_founded": year_founded,
            "employee": employee,
            "capital": capital,
            "revenue": revenue,
            "working_time_start": working_time_start,
            "working_time_end": working_time_end,
            "salary": salary,
            "benefit": benefit,
            "motto": motto,
            "business": business,
            "note": note,
        }
    )
    [sheet.sub_domain.add(x.id) for x in sub_domain]
    [sheet.prefectures.add(x.id) for x in offices]
    sheet.save()

    return redirect("core:main")  # JsonResponse({"status": True})


@login_required
def toggle_favorite(request):
    company_id = request.GET.get("companyId")
    if not company_id:
        return JsonResponse({"status": False})

    user = get_object_or_404(CustomUser, username=request.user.username)
    try:
        sheet = user.created_sheet.get(company_id=company_id)
    except CompanySheet.DoesNotExist:
        return JsonResponse({"status": False})
    sheet.is_favorite = not sheet.is_favorite
    sheet.save()
    return JsonResponse({"status": True, "data": sheet.is_favorite})
