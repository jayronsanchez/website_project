from datetime import timedelta
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView,
                                  RedirectView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from inventory import models

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('inventory.add_category') # permissions. format is <app_name>.<code_permission>
    model = models.Category
    template_name = 'inventory/category/category_form.html'
    fields = ('category_name', 'category_image')

class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('inventory.change_category')
    model = models.Category
    template_name = 'inventory/category/category_form.html'
    fields = ('category_name', 'category_image')

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('inventory.delete_category')
    model = models.Category
    template_name = 'inventory/category/category_confirm_delete.html'
    success_url = reverse_lazy('inventory:system_tailoring_category_list')

class CategoryListView(ListView):
    model = models.Category
    template_name = 'inventory/category/category_list.html'

class CategoryDetailView(DetailView):
    model = models.Category
    template_name = 'inventory/category/category_detail.html'

class ItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # default template name:item_form
    permission_required = ('inventory.add_item')
    model = models.Item
    template_name = 'inventory/item/item_form.html'
    fields = ('item_category', 'item_name', 'item_description', 'item_price', 'item_condition', 'item_image')

class ItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('inventory.change_item')
    model = models.Item
    template_name = 'inventory/item/item_form.html'
    fields = ('item_category', 'item_name', 'item_description', 'item_price', 'item_condition', 'item_image')

class ItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('inventory.delete_item')
    model = models.Item
    template_name = 'inventory/item/item_confirm_delete.html'
    # if delete success, go back to the list.
    success_url = reverse_lazy('inventory:system_tailoring_item_list')

class ItemListView(ListView):
    model = models.Item
    template_name = 'inventory/item/item_list.html'

class ItemDetailView(DetailView):
    model = models.Item
    template_name = 'inventory/item/item_detail.html'
    list_users = []

    def get_context_data(self, **kwargs):
        try:
            self.dibs_user = models.UserDibs.objects.select_related('user').filter(item__id__iexact=self.kwargs.get('pk'))
        except models.UserDibs.DoesNotExist:
            messages.error(self.request, 'Users not found!')
        context = super().get_context_data(**kwargs)
        # clear the list first!
        self.list_users = [] 
        # collect users by order of entry in the UserDibs database
        for user_dibs in self.dibs_user:
            self.list_users.append(user_dibs.user)
        context['user_list'] = self.list_users
        if len(self.list_users) > 0:
            self.dibs = models.UserDibs.objects.filter(user=self.list_users[0], item=self.kwargs.get('pk')).get()
            context['expiry_date'] = self.dibs.user_dibs_expiry_date
        return context

class DibsListView(ListView):
    model = models.UserDibs
    template_name = 'inventory/item/item_list.html'    

    user_dibs_items = []

    def get_queryset(self):
        try:
            self.dibs_user = models.UserDibs.objects.select_related('user').filter(user__username__iexact=self.kwargs.get('username'))
        except models.UserDibs.DoesNotExist:
            messages.error(self.request, 'Users not found!')
        else:
            return self.dibs_user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # clear the list first!
        self.user_dibs_items = []
        # collect item per user
        for user_dibs in self.dibs_user:
            self.user_dibs_items.append(user_dibs.item)
        context['item_list'] = self.user_dibs_items
        return context

class DibsUpdateView(LoginRequiredMixin, UpdateView):
    model = models.UserDibs
    template_name = 'inventory/item/item_dibs_form.html'
    fields = ('user_receipt', 'user_instructions')

class ItemDibs(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('inventory:detail_item', kwargs={'pk':self.kwargs.get('pk')})
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(models.Item, pk=self.kwargs.get('pk'))
        if item.item_dibs_count < 3:
            try:
                models.UserDibs.objects.create(user=self.request.user, item=item)
                #dibs = models.UserDibs.objects.filter(user=self.request.user, item=self.kwargs.get('pk')).get()                
                dibs = get_object_or_404(models.UserDibs, user=self.request.user, item=self.kwargs.get('pk'))
            except IntegrityError:
                messages.warning(self.request, 'Warning! Item already added.')
            else:
                item.item_dibs_count = item.item_dibs_count + 1
                if item.item_dibs_count == 1:
                    dibs.is_user_first = True
                    dibs.user_dibs_expiry_date = timezone.now() + timedelta(days=1)
                    dibs.save()                    
                item.save()
                messages.success(self.request, 'Item added to your list!')
        else:
            messages.error(self.request, 'Max dibs error message')

        return super().get(request, *args, **kwargs)

class ItemUndibs(LoginRequiredMixin, RedirectView):
    user_dibs_list = []

    def get_redirect_url(self, *args, **kwargs):
        return reverse('inventory:detail_item', kwargs={'pk':self.kwargs.get('pk')})
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(models.Item, pk=self.kwargs.get('pk'))
        #self.dibs_user = models.UserDibs.objects.select_related('user').filter(item__id__iexact=self.kwargs.get('pk'))
        user_dibs_list = get_list_or_404(models.UserDibs, item=self.kwargs.get('pk'))
        try:
            dibs = models.UserDibs.objects.filter(
                user=self.request.user,
                item=self.kwargs.get('pk')
            ).get()
        except models.UserDibs.DoesNotExist:
            messages.warning(self.request, 'Item not in your list!')
        else:
            if dibs.is_user_first:
                if len(user_dibs_list) > 1:
                    user_dibs_list[1].user_dibs_expiry_date = timezone.now() + timedelta(days=1)
                    user_dibs_list[1].is_user_first = True
                    user_dibs_list[1].save()
            dibs.delete()            
            item.item_dibs_count = item.item_dibs_count - 1
            item.save()
            messages.success(self.request, 'Item removed from your list!')

        return super().get(request, *args, **kwargs)

class SystemTailoringCategory(TemplateView):
    template_name = 'system_tailoring/system_tailoring_category.html'

class SystemTailoringItem(TemplateView):
    template_name = 'system_tailoring/system_tailoring_item.html'

def update_dibs(request, pk):

    """ FUNCTION BASED VIEW
        This will allow the user to upload a receipt and add instructions
    """
    if request.method == 'POST':
        user_dibs = models.UserDibs.objects.filter(user=request.user, item=pk).get()
        return HttpResponseRedirect(reverse('inventory:item_dibs_update', kwargs={'username':request.user.username, 'pk': user_dibs.pk}))

# save upload_receipt method for future reference when uploading files!
# def upload_receipt(request, pk):

#     """ FUNCTION BASED VIEW
#         This will allow the first dibs user to upload a receipt
#     """
#     if request.method == 'POST':   
#         user_dibs = models.UserDibs.objects.filter(user=request.user, item=pk).get()
#         user_dibs.user_receipt = request.FILES['fileToUpload']
#         user_dibs.save()  
        
#         return HttpResponseRedirect(reverse('inventory:detail_item', kwargs={'pk': pk}))
