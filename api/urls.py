from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("sheet_list", views.get_sheet_list, name="get_sheet_list"),
    path("sheet_detail", views.get_sheet_detail, name="get_sheet_detail"),
    path("company_data", views.get_company_data, name="get_company_data"),
    path("add_sheet", views.add_sheet, name="add_sheet"),
    path("toggle_favorite", views.toggle_favorite, name="set_favorite"),
]
