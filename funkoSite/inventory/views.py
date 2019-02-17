# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.views.generic import (View, TemplateView,
#                                   ListView, DetailView,
#                                   CreateView, UpdateView,
#                                   DeleteView)
# from django.http import HttpResponse
# from . import models

# # Create your views here.

# # Simple class based view
# # class CBView(View):
# #     def get(self, request):
# #         return HttpResponse("Class Based Views Are Cool!")

# class IndexView(TemplateView):
#     # will look into TEMPLATE_DIR in settings.py
#     template_name = 'index.html'

#     # keyword arguments. ** (double asterisk) will accept parameter as a dictionary
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['injectme'] = 'BASIC INJECTION'
#         return context

# class SchoolListView(ListView):
#     model = models.School
#     # returns school_list by default to be used for template tag
#     # default naming of django: lower case the model name, then add _list...
#     # if you want to rename school_list...
#     context_object_name = 'schools'
#     # i think you may assign a template_name also, but by default it would be school_list.html  

# class SchoolDetailView(DetailView):
#     # rename the default return 'school' to be used for template tag
#     context_object_name = 'school_detail'
#     model = models.School
#     # this will look into templates folder of the application
#     template_name = 'basic_app/school_detail.html'

# class SchoolCreateView(CreateView):
#     # default template name school_form.html
#     fields = ('name', 'principal', 'location')
#     model = models.School

# class SchoolUpdateView(UpdateView):
#     fields = ('name', 'principal')
#     model = models.School

# class SchoolDeleteView(DeleteView):
#     model = models.School
#     # if delete success, go back to the list
#     success_url = reverse_lazy('basic_app:list')


# from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)
# from django.http import HttpResponse
from inventory import models

class CategoryCreateView(CreateView):
    model = models.Category
    fields = ('category_name', 'category_image')

class CategoryUpdateView(UpdateView):
    model = models.Category
    fields = ('category_name', 'category_image')

class CategoryDeleteView(DeleteView):
    model = models.Category
    # if delete success, go back to the list. Default template name is category_confirm_delete
    success_url = reverse_lazy('inventory:system_tailoring_category_list')

class CategoryListView(ListView):
     model = models.Category
#     # returns school_list by default to be used for template tag
#     # default naming of django: lower case the model name, then add _list...
#     # if you want to rename school_list...
#     context_object_name = 'schools'
#     # i think you may assign a template_name also, but by default it would be school_list.html

class CategoryDetailView(DetailView):
#     # rename the default return 'school' to be used for template tag
#     context_object_name = 'school_detail'
     model = models.Category
#     # this will look into templates folder of the application
#     template_name = 'basic_app/school_detail.html'


# class CategoryView(View):
#     form_class = forms.CategoryForm
#     success_url = reverse_lazy('home')

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, 'inventory/category_form.html', {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)
#         print("post")
#         if form.is_valid():
#             print("test")
#             if 'category_image' in request.FILES:
#                 models.Category.profile_pic = request.FILES['category_image']
#             form.save()
#             return redirect(self.success_url)
#         else:
#             return render(request, 'inventory/category_form.html', {'form': form})

class ItemCreateView(CreateView):
    # default template name:item_form
    model = models.Item
    fields = ('item_category', 'item_name', 'item_description', 'item_price', 'item_condition', 'item_image')

class ItemUpdateView(UpdateView):
    model = models.Item
    fields = ('item_category', 'item_name', 'item_description', 'item_price', 'item_condition', 'item_image')

class ItemDeleteView(DeleteView):
    model = models.Item
    # if delete success, go back to the list. Default template name is category_confirm_delete
    success_url = reverse_lazy('inventory:system_tailoring_item_list')

class ItemListView(ListView):
    model = models.Item

class SystemTailoringCategory(TemplateView):
    template_name = 'system_tailoring\system_tailoring_category.html'

class SystemTailoringItem(TemplateView):
    template_name = 'system_tailoring\system_tailoring_item.html'
