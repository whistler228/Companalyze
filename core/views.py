from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required

from account.models import CustomUser
from .models import *
from .data_list import prefectures


def top_page(request):
    if request.user.is_authenticated:
        return redirect("core:main")
    return render(request, "core/top_page.html")


@login_required
def main_page(request):
    return render(request, "core/main_page.html")


@login_required
def sheet_detail(request, company_id):
    user = get_object_or_404(CustomUser, username=request.user.username)
    sheet = user.created_sheet.filter(company_id=company_id).first()
    sub_domain = sheet.sub_domain.all()
    return render(request, "core/sheet_detail.html", {"sheet": sheet, "sub_domain": sub_domain})


@login_required
def sheet_edit(request, company_id):
    user = get_object_or_404(CustomUser, username=request.user.username)
    sheet = user.created_sheet.filter(company_id=company_id).first()
    main_domain_all = MainDomain.objects.all()
    sub_domain_all = SubDomain.objects.all()
    main_domain_id = sheet.main_domain.id
    sub_domain_id = sheet.sub_domain.all().values_list("id", flat=True)
    prefectures_name = sheet.prefectures.all().values_list("name", flat=True)

    return render(request, "core/sheet_edit.html",
                  {"sheet": sheet,
                   "main_domain_all": main_domain_all,
                   "sub_domain_all": sub_domain_all,
                   "main_domain_id": main_domain_id,
                   "sub_domain_id": sub_domain_id,
                   "prefectures": prefectures,
                   "prefectures_name": prefectures_name,
                   }
                  )


@login_required
def sheet_add(request):
    main_domain = MainDomain.objects.all()
    sub_domain = SubDomain.objects.all()

    return render(request, "core/sheet_add.html",
                  {"main_domain": main_domain, "sub_domain": sub_domain, "prefectures": prefectures})
