from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.top_page, name="top_page"),
    path("main", views.main_page, name="main"),
    path("sheet/add", views.sheet_add, name="sheet_add"),
    path("sheet/<slug:company_id>", views.sheet_detail, name="sheet"),
    path("sheet/<slug:company_id>/edit", views.sheet_edit, name="sheet_edit"),
]
