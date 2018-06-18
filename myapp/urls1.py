from django.conf.urls import url
from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    url(r'about/', views.about, name='about'),
    url(r'^cat_no/(?P<cat_no>[0-9]+)/$', views.detail, name='detail'),
    url(r'^products/$', views.products, name='products'),
    url(r'^place_order/$', views.place_order, name='place order'),
    url(r'^products/(?P<prod_id>[0-9]+)/$', views.productdetail, name='product details'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^myorders/$', views.myorders, name='myorders'),
    url(r'^upload/$', views.upload_form, name='upload'),
    # url(r'forgotpass/$', views.forgotpass, name='forgotpass'),

    ]

