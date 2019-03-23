from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView,
                                  RedirectView)
from inventory import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError

class CategoryCreateView(CreateView):
    model = models.Category
    fields = ('category_name', 'category_image')

class CategoryUpdateView(UpdateView):
    model = models.Category
    fields = ('category_name', 'category_image')

class CategoryDeleteView(DeleteView):
    model = models.Category
    success_url = reverse_lazy('inventory:system_tailoring_category_list')

class CategoryListView(ListView):
    model = models.Category

class CategoryDetailView(DetailView):
    model = models.Category

class ItemCreateView(CreateView):
    # default template name:item_form
    model = models.Item
    fields = ('item_category', 'item_name', 'item_description', 'item_price', 'item_condition', 'item_image')

class ItemUpdateView(UpdateView):
    model = models.Item
    fields = ('item_category', 'item_name', 'item_description', 'item_price', 'item_condition', 'item_image')

class ItemDeleteView(DeleteView):
    model = models.Item
    # if delete success, go back to the list.
    success_url = reverse_lazy('inventory:system_tailoring_item_list')

class ItemListView(ListView):
    model = models.Item

class ItemDetailView(DetailView):
    model = models.Item
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

        return context


class DibsListView(ListView):
    model = models.UserDibs
    template_name = 'inventory/item_list.html'    

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


class ItemDibs(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('inventory:detail_item', kwargs={'pk':self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(models.Item, pk=self.kwargs.get('pk'))
        try:
            models.UserDibs.objects.create(user=self.request.user, item=item)
        except IntegrityError:
            messages.warning(self.request, 'Warning! Item already added.')
        else:
            messages.success(self.request, 'Item added to your list!')

        return super().get(request, *args, **kwargs)

class ItemUndibs(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('inventory:detail_item', kwargs={'pk':self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        try:
            dibs = models.UserDibs.objects.filter(
                user=self.request.user,
                item=self.kwargs.get('pk')
            ).get()
        except models.UserDibs.DoesNotExist:
            messages.warning(self.request, 'Item not in your list!')
        else:
            dibs.delete()
            messages.success(self.request, 'Item removed from your list!')

        return super().get(request, *args, **kwargs)

class SystemTailoringCategory(TemplateView):
    template_name = 'system_tailoring/system_tailoring_category.html'

class SystemTailoringItem(TemplateView):
    template_name = 'system_tailoring/system_tailoring_item.html'
