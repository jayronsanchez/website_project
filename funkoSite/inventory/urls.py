from django.urls import path, include
from inventory import views

app_name = 'inventory'

urlpatterns = [
    # for system_tailoring
    #  apply RESTful architecture ea: /categories/<int>
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
    #for category
    #  apply RESTful architecture ea: /categories/<int>
    path('categories/', views.CategoryListView.as_view(), name='list_category'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='detail_category'),
    # for items
    #  apply RESTful architecture ea: /items/<int>
    path('items/', views.ItemListView.as_view(), name='list_item'),    
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='detail_item'),    
    path('items/dibs/<int:pk>', views.ItemDibs.as_view(), name='item_dibs'),    
    path('items/undibs/<int:pk>', views.ItemUndibs.as_view(), name='item_undibs'),
    # for user dibs
    #  apply RESTful architecture ea: /<username>/items/<item:id>
    path('<username>/my_items', views.DibsListView.as_view(), name='item_dibs_list'),     
    path('items/<int:pk>/form', views.update_dibs, name='item_dibs_update_redirect'),
    path('<username>/my_items/item/<int:pk>', views.DibsUpdateView.as_view(), name='item_dibs_update'),
]
