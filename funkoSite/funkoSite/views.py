
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)
from django.http import HttpResponse
from inventory import models

class IndexView(TemplateView):
    template_name = 'home.html'

class SystemTailoring(TemplateView):
    template_name = 'system_tailoring/system_tailoring.html'

class WelcomeAdminView(TemplateView):
    template_name = 'welcome_user.html'

class ThanksView(TemplateView):
    template_name = 'thanks.html'

class AboutView(TemplateView):
    template_name = 'about.html'
