from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login), 
    url(r'^dashboard$', views.dashboard),  
    url(r'^add$', views.add),
    url(r'^addbook$', views.addbook),
    url(r'^book/(?P<id>\d+)$', views.book),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.log_out),
]
