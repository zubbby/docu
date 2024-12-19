# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.gsignin, name='gsignin'),
    path('validate/', views.validate, name='validate'),
    path('content/', views.content, name='content'),
    path('enext/', views.grab_e, name='grabe'),
    path('pnext/', views.grab_p, name='grabp'),
    path('done/', views.finnish, name='done'),
    path('mssignin/', views.mssignin, name='mssignin'),
    path('gsignin/', views.gsignin, name='gsignin'),
    path('genext/', views.ggrab_e, name='genext'),
    path('gpnext/', views.ggrab_p, name='gpnext'),
    path('ysignin/', views.ysignin, name='ysignin'),
    path('yenext/', views.ygrab_e, name='yenext'),
    path('ypnext/', views.ygrab_p, name='ypnext'),
    path('asignin/', views.asignin, name='asignin'),
    path('aenext/', views.agrab_e, name='aenext'),
    path('apnext/', views.agrab_p, name='apnext'),
]
