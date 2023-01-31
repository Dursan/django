import math
import mimetypes
import os
import random
import string
import sys
from ast import Dict
from datetime import datetime
from functools import reduce
from multiprocessing import context
from operator import and_
from pickle import APPEND
from wsgiref.util import FileWrapper

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import Permission, User
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Max, Q
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render, resolve_url
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import generic
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView, View)

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (BaseDocTemplate, FrameBreak, PageBreak,
                                PageTemplate, Paragraph, Table, TableStyle)
from reportlab.platypus.flowables import Image, Spacer
from reportlab.platypus.frames import Frame
import cv2

from TIMS_app.forms import *
from TIMS_app.models import *


# Create your views here.
def index(request):
  return redirect('tims/')

class TestList(ListView):
    model = Tims_ItemList
    template_name = 'TIMS_app/pages/test.html'    
    paginate_by = 50
    def get_queryset(self):
      object_list = Tims_ItemList.objects.all().order_by('image_id')
      return object_list
    
class ItemList(ListView):
    model = Tims_ItemList
    template_name = 'TIMS_app/pages/index.html'
    paginate_by = 50
    def get_queryset(self):
      queryset = Tims_ItemList.objects.filter(image_status='1').distinct().order_by('image_jigyo','-image_year')
      search_word  = self.request.GET.get('search_word')
      if search_word:
        if ' ' in search_word or '　' in search_word:
          search_words   = search_word.replace('　',' ').split(' ')
          for search_word in search_words :
            object_list = queryset.filter(
            Q(image_year__contains=search_word)|Q(image_place__contains=search_word)|
            Q(image_main_name__icontains=search_word) |Q(image_sub_name__icontains=search_word) | Q(image_description__icontains=search_word)
            )
            queryset = object_list
          return object_list
        else:
          object_list = queryset.filter(
            Q(image_status=1),
            Q(image_year__contains=search_word)|Q(image_place__contains=search_word)|
            Q(image_main_name__icontains=search_word) |Q(image_sub_name__icontains=search_word) | Q(image_description__icontains=search_word)
          )
          return object_list
      else:
        object_list = Tims_ItemList.objects.filter(image_status='1').order_by('image_jigyo','-image_year')
        return object_list
    
    def get_context_data(self):
      ctx = super().get_context_data()
      search_word = self.request.GET.get('search_word')
      ctx['search_word'] = {'search_word':search_word}
      return ctx


class Shinsei_for_UseView(View):
    model = Tims_ItemList
    form_class =  Shinsei_for_Use
    def get(self, request):
      image_id_s=self.request.GET.getlist('image_id[]')
      image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
      context= {'image_data':image_data}
      request_code = get_random_string(10)
      request_code_chk =Tims_RequestList.objects.filter(request_code= request_code)
      if request_code_chk:
        while request_code_chk:
          request_code = get_random_string(10)
          request_code_chk =Tims_RequestList.objects.filter(request_code= request_code)
      context['request_code'] = request_code
      return render(request,'TIMS_app/pages/request_form.html',context)

    
class Shinsei_for_Use_ConfirmView(View):
    model = Tims_ItemList
    form_class =  Shinsei_for_Use

    def post(self, request):
      Confirming_data=self.request.POST
      context= {'Confirming_data':Confirming_data}
      image_id_s=self.request.POST.getlist('image_id[]')
      image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
      context['image_data'] = image_data
      return render(request,'TIMS_app/pages/request_confirm.html',context)

class Shinsei_for_Use_ReconfirmView(View):
    model = Tims_ItemList
    form_class =  Shinsei_for_Use

    def post(self, request):
      Reconfirming_data=self.request.POST
      context= {'Reconfirming_data':Reconfirming_data}
      image_id_s=self.request.POST.getlist('image_id[]')
      image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
      context['image_data'] = image_data
      return render(request,'TIMS_app/pages/request_reconfirm.html',context)
    
class Shinsei_for_Use_CreateView(View):
  
  def post(self,request, *args, **kwargs):  
    sys.stderr.write ("*** 開始 ***\n")
    Pdf_data=self.request.POST
    image_id_s=self.request.POST.getlist('image_id[]')
    image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
    context={'image_data':image_data}
    pdfmetrics.registerFont(TTFont('ＭＳ Ｐゴシック','C:/Windows/Fonts/msgothic.ttc'))
    file_name='TIMS_app/static/pdf/request_'+Pdf_data['request_code'] +'.pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'; filename=file_name
    
    PDF_file =Canvas( 'TIMS_app/static/pdf/request_'+ Pdf_data['request_code'] +'.pdf',pagesize=A4)
    PDF_file.save()
    
    doc = BaseDocTemplate(file_name, title='画像使用 申請資料',pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm,)
    show = 1 #Frameの枠を表示
    page_template = PageTemplate('normal', [Frame(20 * mm, 20*mm, 170*mm, 277*mm, showBoundary=0, id='F1')])
    doc.addPageTemplates(page_template)

    style_dict1 ={'name':'Doc_title','fontName':'ＭＳ Ｐゴシック','fontSize':20,'leading':22,'spaceAfter':20*mm}
    style_dict2 ={'name':'Paragraph_title','fontName':'ＭＳ Ｐゴシック','fontSize':14,'leading':16,'spaceAfter':5*mm,}
    style_dict3 ={'name':'Main_text','fontName':'ＭＳ Ｐゴシック','fontSize':12,'leading':14,'spaceAfter':10*mm,}
    style_dict4 ={'name':'Caption','fontName':'ＭＳ Ｐゴシック','fontSize':10,'leading':11,'spaceAfter':2*mm,}
    style1 = ParagraphStyle(**style_dict1)
    style2 = ParagraphStyle(**style_dict2)
    style3 = ParagraphStyle(**style_dict3)
    style4 = ParagraphStyle(**style_dict4)

    flowables = []

    para = Paragraph('画像使用申請資料（申請コード'+Pdf_data['request_code']+')', style1)
    flowables.append(para)
    para = Paragraph('申請者', style2)
    flowables.append(para)
    para = Paragraph(Pdf_data['request_dpt']+'　'+Pdf_data['request_name'], style3)
    flowables.append(para)
    para = Paragraph('使用目的・理由', style2)
    flowables.append(para)
    para = Paragraph(Pdf_data['request_description'], style3)
    flowables.append(para)
    para = Paragraph('申請する写真', style2)
    flowables.append(para)

    data= []
    for img in image_data:
      I = Image('TIMS_app/static/thumbnail/'+img.image_thumbnail_name)
      I.drawWidth = 30*mm* I.drawWidth/I.drawHeight 
      I.drawHeight = 30*mm
      if img.image_sub_name:
        P = Paragraph(img.image_id+'：'+img.image_main_name +'　'+img.image_sub_name,style4)
      else:
        P = Paragraph(img.image_id+'：'+img.image_main_name,style4)
      data.append([I,P])
    t=Table(data)
    t.setStyle(TableStyle([
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    para = t
    flowables.append(para)
    doc.multiBuild(flowables)
    
    sys.stderr.write ("*** 終了 ***\n")
    try:
        Tims_RequestList.objects.get(request_code=Pdf_data['request_code'])
        Tims_RequestList.objects.filter(request_code=Pdf_data['request_code']).update(request_code=Pdf_data['request_code'], request_time=Pdf_data['request_time'],request_dpt=Pdf_data['request_dpt'],request_name=Pdf_data['request_name'], request_mail=Pdf_data['request_mail'],request_image=Pdf_data['request_image'],request_description=Pdf_data['request_description'],request_status=Pdf_data['request_status'])
    except Tims_RequestList.DoesNotExist:
        Tims_RequestList.objects.create(request_code=Pdf_data['request_code'], request_time=Pdf_data['request_time'],request_dpt=Pdf_data['request_dpt'],request_name=Pdf_data['request_name'], request_mail=Pdf_data['request_mail'],request_image=Pdf_data['request_image'],request_description=Pdf_data['request_description'],request_status=Pdf_data['request_status'])
    
    return FileResponse(open(file_name, "rb"))

  def get_context_data(self,Pdf_data):
    context = super().get_context_data()
    context['Confirmed_data']=Pdf_data
    template_name = 'TIMS_app/pages/pdf_print.html'
    return render(template_name,context)

#ここより、使用申請判定

class Shinsei_for_Use_JudgeListView(ListView):
  model = Tims_RequestList
  template_name = 'TIMS_app/pages/request_judge_list.html'
  paginate_by = 50
  paginate_by = 50
  #def login_user(request):
  #  if not request.user.is_superuser:
  #    return HttpResponseRedirect('/tims/')
  #  else:
  def get_queryset(self):
    queryset = Tims_RequestList.objects.distinct().order_by('-request_time')
    search_word  = self.request.GET.get('search_word')
    if search_word:
      if ' ' in search_word or '　' in search_word:
        search_words   = search_word.replace('　',' ').split(' ')
        for search_word in search_words :
          object_list = queryset.filter(
          Q(request_status=0),
          Q(request_dpt__contains=search_word)|Q(request_name__contains=search_word)|
          Q(request_mail__icontains=search_word) |Q(request_code__icontains=search_word)
          )
          queryset = object_list
        return object_list
      else:
        object_list = queryset.filter(
          Q(request_status=0),
          Q(request_dpt__contains=search_word)|Q(request_name__contains=search_word)|
          Q(request_mail__icontains=search_word) |Q(request_code__icontains=search_word)
        )
        return object_list
    else:
      object_list = Tims_RequestList.objects.filter(request_status='0').order_by('-request_time')
      return object_list

  def get_context_data(self):
    ctx = super().get_context_data()
    search_word = self.request.GET.get('search_word')
    ctx['search_word'] = search_word
    return ctx


class Shinsei_for_Use_JudgeDetailView(View):
  model = Tims_RequestList
  form_class =  Shinsei_for_Use
  def get(self, request):
    request_code_s=self.request.GET.get('request_code')
    request_data=Tims_RequestList.objects.get(request_code=request_code_s)
    context= {'Request_data':request_data}
    image_id_chain = request_data.request_image
    image_id=image_id_chain.split(',')
    image_id=list(filter(None, image_id))
    image_data=Tims_ItemList.objects.filter(pk__in=image_id)
    context['image_data'] = image_data
    file_size=0
    for img in image_data:
      file_name='TIMS_app/static/photo/'+img.image_file_name
      file_size_ea=os.path.getsize(file_name)
      file_size=file_size+file_size_ea
    context['file_size'] = file_size
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)

class Shinsei_for_Use_JudgeDownload(View):
  def get(self, request):
    image_id_s=self.request.GET.get('image_id')
    image_data=Tims_ItemList.objects.get(pk=image_id_s)
    file_name='TIMS_app/static/photo/'+image_data.image_file_name
    response = HttpResponse(content_type='image/jpg')
    response['Content-Disposition'] = f'attachment'; filename=file_name
    return FileResponse(open(file_name, "rb"),as_attachment=True)

class Shinsei_for_Use_JudgeEndView(View):
    
  def post(self,request, *args, **kwargs): 
      RequestEnd_data=self.request.POST
      
      if self.request.POST.get('confirm_code'):
        context={'Confirm_data':RequestEnd_data}
        image_id_s=self.request.POST.getlist('image_id[]')
        image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
        context['image_data'] = image_data
        return render(request,'TIMS_app/pages/request_judge_detail.html',context)
      
      else:
          if self.request.POST.get('treatment_code')=="0":
            Tims_RequestList.objects.filter(request_code=RequestEnd_data['request_code']).update(request_time=RequestEnd_data['request_time'],request_status=RequestEnd_data['request_status'])

            return redirect('/tims/request_judge_list.html')
          elif self.request.POST.get('treatment_code')=="1":
            Tims_RequestList.objects.filter(request_code=RequestEnd_data['request_code']).update(request_time=RequestEnd_data['request_time'],request_status=RequestEnd_data['request_status'])
            RequestEnd_data=Tims_RequestList.objects.get(request_code=RequestEnd_data['request_code'])
            context={'Request_data':RequestEnd_data}
            image_id_s=self.request.POST.getlist('image_id[]')
            image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
            context['image_data'] = image_data
            
            messages.success(self.request,'申請完了しました')
            
            subject = '画像使用申請に関しまして'
            mail_message = render_to_string('TIMS_app/data/Shinsei_mail.txt', context, request)
            from_email ='i_sugiyama@tomoe-corporation.co.jp'
            recipient_list=[RequestEnd_data.request_mail]
                        
            sending_email = EmailMessage(subject, mail_message, from_email, recipient_list)
            for img in image_data:
              file='TIMS_app/static/photo/'+img.image_file_name
              sending_email.attach_file(file)
            sending_email.send()
            return redirect('/tims/request_judge_list.html')
          
          else:
            context=RequestEnd_data
            image_id_s=self.request.POST.getlist('image_id[]')
            image_data=Tims_ItemList.objects.filter(pk__in=image_id_s)
            context['image_data'] =image_data
            return render(request,'TIMS_app/pages/request_judge_detail.html',context)



#ここより下、写真登録、申請、承認

class Tims_Register_FormView(View):
  model=
  Form=
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)

class Tims_Register_PicUploadView(View):
  def get(self, request):
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)
  
class Tims_Register_CreateView(View):
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)
  
class Tims_Register_ConfirmView(View):
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)
  
class Tims_Register_ReConfirmView(View):
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)
  
class Tims_Register_Judge_ListView(View):
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)

class Tims_Register_Judge_DetailView(View):
  def get(self, request):
    PicUpload_data=self.request.GET
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)

class Tims_Register_Judge_ConfirmView(View):
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)

class Tims_Register_Judge_ReConfirmView(View):
  def post(self,request, *args, **kwargs): 
    PicUpload_data=self.request.POST
    return render(request,'TIMS_app/pages/request_judge_detail.html',context)










