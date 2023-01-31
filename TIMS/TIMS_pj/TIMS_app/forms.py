import json
from TIMS_app.models import *
from django.forms import HiddenInput,ModelForm
from django import forms

class Shinsei_for_Use(forms.ModelForm):

  request_code =  forms.CharField(max_length=255)
  request_time =  forms.CharField(max_length=255)
  request_dpt =  forms.CharField(max_length=255)
  request_name =  forms.CharField(max_length=255)
  request_mail =  forms.CharField(max_length=255)
  request_image =  forms.CharField(max_length=255)
  request_description =  forms.CharField(max_length=255)
  request_status =  forms.CharField(max_length=255)

  class Meta:
      model =  Tims_RequestList
      fields = ['request_code','request_time','request_dpt','request_name','request_mail','request_image','request_description','request_status']


class Register_data(forms.ModelForm):

    image_id = forms.CharField(primary_key=True,unique=True,max_length=255)
    image_main_name = forms.CharField(max_length=255)
    image_sub_name =  forms.CharField(max_length=255)
    image_jigyo =  forms.CharField(max_length=255)
    image_product =  forms.CharField(max_length=255)
    image_year = forms.IntegerField()
    image_place =  forms.CharField(max_length=255)
    image_client =  forms.CharField(max_length=255)
    image_thumbnail_name =  forms.CharField(max_length=255)
    image_file_name =  forms.CharField(max_length=255)
    image_description =  forms.CharField(max_length=255)
    image_status =  forms.CharField(max_length=255)
    image_parson =  forms.CharField(max_length=255)
    image_timestamp =  forms.CharField(max_length=255)
    image_dpt =  forms.CharField(max_length=255)

  class Meta:
      model =  Tims_RequestList
      fields = ['image_id',
                'image_main_name',
                'image_sub_name',
                'image_jigyo',
                'image_product',
                'image_year',
                'image_place',
                'image_client',
                'image_thumbnail_name',
                'image_file_name',
                'image_description',
                'image_status',
                'image_parson',
                'image_timestamp',
                'image_dpt']