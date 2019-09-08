from django.urls import path
from . import views # import all views in views file inside app(this) folder

app_name = 'app'

urlpatterns = [


    #url for home view in app views
    path('home/', views.home, name ='home'),


    #url for simple_render view in app views
    path('simple/', views.simple_render, name='simple'),


    #url for simple_render_with_context view in app views
    path('simple/context/', views.render_with_context, name='simple'),


    #url for simple_list view in app views
    path('simple/list/', views.simple_list, name='simple-list'),


    #url for simple_detail view in app views
    path('simple/detail/', views.simple_detail, name='simple-detail'),

    #url for store list view in app views
    path('list/', views.store_list, name='list'),


    #url for store detail view in app views containing store_slug of slug type
    path('detail/<slug:store_slug>', views.store_detail, name='detail'),


    #url for store create view in app views
    path('create/', views.store_create, name='create'),


    #url for store update view in app views containing store_slug of slug type
    path('update/<slug:store_slug>', views.store_update, name='update'),


	#url for store delete view in app views containing store_slug of slug type
    path('delete/<slug:store_slug>', views.store_delete, name='delete'),


    #url for signup view in app views
    path('signup/', views.signup, name='signup'),


    #url for signin view in app views
    path('signin/', views.signin, name='signin'),


    #url for signout view in app views
    path('signout/', views.signout, name='signout'),


    #url for item create view in app views containing store_slug of slug type
    path('create/item/store/<slug:store_slug>', views.item_create, name='item-create'),


    #url for item update view in app views containing item_slug of slug type
    path('update/item/<slug:item_slug>', views.item_update, name='item-update'),


    #url for store delete view in app views containing item_slug of slug type
    path('delete/item/<slug:item_slug>', views.item_delete, name='item-delete'),
]