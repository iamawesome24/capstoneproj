from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.homepage, name='dashboard'),
    path('result/', views.results, name='result'),
    path('overview/', views.profile, name='overview'),
    path('new/', views.addpatient, name='addPatient'),

    #path('overview/predict/', views.predict, name='predict'),
]