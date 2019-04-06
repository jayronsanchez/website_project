from django.urls import path, include
from inventory import views

app_name = 'inventory'

urlpatterns = [
    path('system_tailoring/category/', views.SystemTailoringCategory.as_view(), name='system_tailoring_category'),
    path('system_tailoring/category/create_category/', views.CategoryCreateView.as_view(), name='create_category'),
    path('system_tailoring/category/category_list/', views.CategoryListView.as_view(template_name='system_tailoring/system_tailoring_category_list.html'), name='system_tailoring_category_list'),
    path('system_tailoring/category/<int:pk>/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('system_tailoring/category/remove/<int:pk>/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('system_tailoring/item/', views.SystemTailoringItem.as_view(), name='system_tailoring_item'),
    path('system_tailoring/item/create_item/', views.ItemCreateView.as_view(), name='create_item'),
    path('system_tailoring/item/item_list/', views.ItemListView.as_view(template_name='system_tailoring/system_tailoring_item_list.html'), name='system_tailoring_item_list'),
    path('system_tailoring/item/<int:pk>/', views.ItemUpdateView.as_view(), name='update_item'),
    path('system_tailoring/item/remove/<int:pk>/', views.ItemDeleteView.as_view(), name='delete_item'),
    path('list_category/', views.CategoryListView.as_view(), name='list_category'),
    path('list_category/<int:pk>/', views.CategoryDetailView.as_view(), name='detail_category'),
    path('list_item/', views.ItemListView.as_view(), name='list_item'),
    path('list_item/<int:pk>', views.ItemDetailView.as_view(), name='detail_item'),
    path('list_item/<int:pk>/upload_receipt', views.upload_receipt, name='detail_item_upload_receipt'),
    path('list_item/dibs/<int:pk>', views.ItemDibs.as_view(), name='item_dibs'),
    path('list_item/undibs/<int:pk>', views.ItemUndibs.as_view(), name='item_undibs'),
    path('my_items/<username>', views.DibsListView.as_view(), name='item_dibs_list'), 
]