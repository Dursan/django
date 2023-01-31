import random
import string

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import Permission, User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Max, Q
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView, View)
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

#from TIMS_app.forms import *
from TIMS_app.models import *

# Create your views here.


class ItemList(ListView):
    model = Tims_ItemList
    template_name = 'TIMS_pj/TIMS_app/pages/index.html'
    paginate_by = 20

    def get_queryset(self):
      search_word  = self.request.GET.get('search_word')
      user_id = self.request.user.id
      if user_id:
        if search_word:
          object_list = Tims_ItemList.objects.filter(Q(image_status=1)|Q(image_status=0),Q(image_jword__icontains=search_word) | Q(image_jigyo__icontains=search_word) | Q(image_jdescription__icontains=search_word)).distinct().order_by('image_status','image_jigyo')
        else:
          object_list = Tims_ItemList.objects.filter(Q(image_status=1)|Q(image_status=0)).order_by('image_jigyo','image_jigyo')
        return object_list
      else:
        if search_word:
          object_list = Tims_ItemList.objects.filter(Q(image_status=1),Q(image_jword__icontains=search_word) | Q(image_jigyo__icontains=search_word) | Q(image_jdescription__icontains=search_word)).distinct().order_by('image_jigyo')
        else:
          object_list = Tims_ItemList.objects.filter(image_status=1).order_by('image_jigyo','image_jigyo')
        return object_list

    def get_context_data(self):
      ctx = super().get_context_data()
      search_word = self.request.GET.get('search_word')
      ctx['search_word'] = {'search_word':search_word}
      return ctx