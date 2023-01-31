"""TIMS_pj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve 

from . import views
from TIMS_app.views import *


app_name = 'TIMS_app'


urlpatterns = [
	path('', views.index, name='index'),
    path('tims/', views.ItemList.as_view(), name='index'),
    path('tims/test.html', views.TestList.as_view(), name='test'),
    path('tims/index.html', views.ItemList.as_view(), name='index_search'),
    path('tims/request_form.html', views.Shinsei_for_UseView.as_view(), name='Shinsei_for_Use'),
    path('tims/request_confirm.html', views.Shinsei_for_Use_ConfirmView.as_view(), name='Shinsei_for_Use_confirm'),
    path('tims/request_reconfirm.html', views.Shinsei_for_Use_ReconfirmView.as_view(), name='Shinsei_for_Use_reconfirm'),
    path('tims/pdf_print.html', views.Shinsei_for_Use_CreateView.as_view(), name='Shinsei_for_Use_create'),
    path('tims/request_judge_list.html', views.Shinsei_for_Use_JudgeListView.as_view(), name='Shinsei_for_Use_judge_list'),
    path('tims/request_judge_detail.html', views.Shinsei_for_Use_JudgeDetailView.as_view(), name='Shinsei_for_Use_judge_detail'),
    path('tims/request_judge_download.html', views.Shinsei_for_Use_JudgeDownload.as_view(), name='Shinsei_for_Use_judge_download'),
    path('tims/request_end_confirm.html', views.Shinsei_for_Use_JudgeEndView.as_view(), name='Shinsei_for_Use_judge_end'),
    path('tims/request_end.html', views.Shinsei_for_Use_JudgeEndView.as_view(), name='Shinsei_for_Use_judge_end'),
    path('tims/register_form.html', views.Tims_Register_PicUploadView.as_view(), name='Register_form'),
    path('tims/register_pic_upload.html', views.Tims_Register_PicUploadView.as_view(), name='Register_pic_Upload'),
    path('tims/register_create.html', views.Tims_Register_CreateView.as_view(), name='Register_create'),
    path('tims/register_confirm.html', views.Tims_Register_ConfirmView.as_view(), name='Register_confirm'),
    path('tims/register_reconfirm.html', views.Tims_Register_ConfirmView.as_view(), name='Register_confirm'),
    path('tims/register_judge_list.html', views.Tims_Register_Judge_ListView.as_view(), name='Register_judge_list'),
    path('tims/register_judge_detail.html', views.Tims_Register_Judge_DetailView.as_view(), name='Register_judge_detail'),
    path('tims/register_judge_confirm.html', views.Tims_Register_Judge_ConfirmView.as_view(), name='Register_judge_confirm'),
    path('tims/register_judge_reconfirm.html', views.Tims_Register_Judge_ReConfirmView.as_view(), name='Register_judge_reconfirm'),
    #re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns