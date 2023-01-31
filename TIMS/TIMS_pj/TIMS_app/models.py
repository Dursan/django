from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Tims_ItemList(models.Model):
    
    class Meta:
       managed = False
       db_table = 'tims_image_list'
    
    image_id = models.CharField(primary_key=True,unique=True,max_length=255)
    image_main_name = models.CharField(max_length=255)
    image_sub_name =  models.CharField(max_length=255)
    image_jigyo =  models.CharField(max_length=255)
    image_product =  models.CharField(max_length=255)
    image_year = models.IntegerField()
    image_place =  models.CharField(max_length=255)
    image_client =  models.CharField(max_length=255)
    image_thumbnail_name =  models.CharField(max_length=255)
    image_file_name =  models.CharField(max_length=255)
    image_description =  models.CharField(max_length=255)
    image_status =  models.CharField(max_length=255)
    image_parson =  models.CharField(max_length=255)
    image_timestamp =  models.CharField(max_length=255)
    image_dpt =  models.CharField(max_length=255)

    def __str__(self):
      return self.image_id
    
    
class Tims_RequestList(models.Model):

   class Meta:
      managed = False
      db_table = 'tims_request_list'

   id = models.AutoField(primary_key=True,unique=True)
   request_code =  models.CharField(max_length=255)
   request_time =  models.CharField(max_length=255)
   request_dpt =  models.CharField(max_length=255)
   request_name =  models.CharField(max_length=255)
   request_mail =  models.CharField(max_length=255)
   request_image =  models.CharField(max_length=255)
   request_description =  models.CharField(max_length=255)
   request_status =  models.CharField(max_length=255)


   def __int__(self):
     return self.id